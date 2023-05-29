import os
import struct
import configparser

class ImageInfo:
    TARGET_TYPE_FLASH = 1
    TARGET_TYPE_XMODEM = 2
    def __init__(self):
        self.imgc_flash = 0
        self.paramc_flash = 0
        self.imgc_xmodem = 0
        self.paramc_xmodem = 0
        self.XMODEM_TO_FLASH = False
        self.NEXT_IMG_START = 0
        self.xmodemBins = []
        self.flashBins = []
        self.flashHeaders = []
        self.xmodemHeaders = []
        self.flashAddressStart = []

def mycrc32(szString):
    m_pdwCrc32Table = [0 for x in range(0,256)]
    dwPolynomial = 0xEDB88320;
    dwCrc = 0
    for i in range(0,256):
        dwCrc = i
        for j in [8,7,6,5,4,3,2,1]:
            if dwCrc & 1:
                dwCrc = (dwCrc >> 1) ^ dwPolynomial
            else:
                dwCrc >>= 1
        m_pdwCrc32Table[i] = dwCrc
    dwCrc32 = 0xFFFFFFFF
    for i in szString:
        b = 0
        if type(i) == type(1):
            b = i
        else:
            b = ord(i)
        dwCrc32 = ((dwCrc32) >> 8) ^ m_pdwCrc32Table[(b) ^ ((dwCrc32) & 0x000000FF)]
    return dwCrc32

def genRootHeader(config, imageInfo, targetType):
    if targetType == imageInfo.TARGET_TYPE_FLASH:
        imgc = imageInfo.imgc_flash
        paramc = imageInfo.paramc_flash
    else:
        imgc = imageInfo.imgc_xmodem
        paramc = imageInfo.paramc_xmodem
    magicNum = int(config.get('productroot', 'MagicNumber'), 16)
    magicNum = struct.pack('I', magicNum)
    product = int(config.get('productroot', 'Product'), 16)
    product = struct.pack('I', product)
    version = int(config.get('productroot', 'Version'))
    version = struct.pack('I', version)
    imgCount = struct.pack('I', imgc)
    paramCount = struct.pack('I', paramc)
    headerSize = 256 + imgc * 64 + paramc * 64
    hdrSize = struct.pack('I', headerSize)
    flashWriteEnable = struct.pack('I', 0)
    if imageInfo.XMODEM_TO_FLASH:
        flashWriteEnable = struct.pack('I', 0xaa5555aa)        
    rootHeader = magicNum + product + version + imgCount + paramCount + hdrSize + flashWriteEnable
    rootHeader += struct.pack('I', 0) * (29 + 28)
    return rootHeader

def genFlashImgHeader(config, section, imageInfo):
    if section[0:4] == 'code':
        imageInfo.imgc_flash += 1
    elif section[0:5] == 'param':
        imageInfo.paramc_flash += 1
    else:
#        print('non section:')
        return
    
    isXmodem = False
    if config.has_option(section, 'Xmodem'):
        isXmodem = True
        if section[0:4] == 'code':
            imageInfo.imgc_xmodem += 1
        elif section[0:5] == 'param':
            imageInfo.paramc_xmodem += 1
        if config.get(section, 'Xmodem') == 'W':
            imageInfo.XMODEM_TO_FLASH = True
            #print('xmodem image(write to flash):')
        else:
            #print('xmodem image:')
            pass

    filePath = config.get(section, 'FilePath')
    imageSize = os.path.getsize(filePath)
    imageSizePacked = struct.pack('I', imageSize)
    binFile = open(filePath, 'rb')
    binData = binFile.read()
    binFile.close()
    if isXmodem:
        imageInfo.xmodemBins.append(binData)
    imageInfo.flashBins.append(binData)

    imageName = config.get(section, 'ImageName')
    strImage = imageName
    imageName = imageName.ljust(32, '\0')
    imageName = imageName.encode('utf-8')

    flashAddr = config.get(section, 'FlashAddress')
    if not flashAddr:
        print('%s FlashAddress is empty, put it at 0x%08x' % (strImage, imageInfo.NEXT_IMG_START))
        flashAddrInt = imageInfo.NEXT_IMG_START
    else:
        flashAddrInt = int(flashAddr, 16)
        if flashAddrInt < imageInfo.NEXT_IMG_START:
            print("%s Flash Address at %s has been taken, put it at 0x%08x" % \
                  (strImage, flashAddr, imageInfo.NEXT_IMG_START))
            flashAddrInt = imageInfo.NEXT_IMG_START
    flashAddrPacked = struct.pack('I', flashAddrInt)
    imageInfo.flashAddressStart.append(flashAddrInt)

    memAddr = config.get(section, 'MemoryAddress')
    memAddr = int(memAddr, 16)
    memAddrPacked = struct.pack('I', memAddr)

    if section[0:4] == 'code':
        entry = config.get(section, 'Entry')
        entry = int(entry, 16)
        entryPacked = struct.pack('I', entry)
    else:      
        entryPacked = struct.pack('I', 0)

    entryType = config.get(section, 'Type')
    entryType = int(entryType, 16)
    entryTypePacked = struct.pack('I', entryType)
    #last one, time to calc next image's start address
    #4k-byte align
    if ((flashAddrInt + imageSize) % 4096):
        imageInfo.NEXT_IMG_START = (int)((flashAddrInt + imageSize) / 4096) * 4096 + 4096
#        print('not 4k-byte align')
    else:
        imageInfo.NEXT_IMG_START = (flashAddrInt + imageSize)
#        print('4k-byte align')
    
    #print('curr image offset:0x%08x' % imageInfo.NEXT_IMG_START)

    crc = mycrc32(binData)
    print('%-24s size: 0x%08x    offset:0x%08x    crc: 0x%08x' % (strImage, imageSize, imageInfo.NEXT_IMG_START, crc))
    #print('crc: %x' % crc)
    imageCRCPacked = struct.pack('I', crc)
    imgReservedPacked = struct.pack('I', 0) + struct.pack('I', 0)
    
    imageHeader = imageName + \
                  imageSizePacked + \
                  flashAddrPacked + \
                  memAddrPacked + \
                  entryPacked + \
                  entryTypePacked + \
                  imageCRCPacked + \
                  imgReservedPacked
    
    if isXmodem:
        imageInfo.xmodemHeaders.append(imageHeader)      
    imageInfo.flashHeaders.append(imageHeader)


def config_to_flash(ini_file, flash_file, xmodem_file):

    print("\ndeal config file: %s"%ini_file)
    config = configparser.ConfigParser()
    config.read(ini_file)
    imageInfo = ImageInfo()

    for section in config.sections():
        genFlashImgHeader(config, section, imageInfo)

    imageInfo.NEXT_IMG_START = 256 + 64 * (imageInfo.imgc_flash + imageInfo.paramc_flash)
    print('HeaderSize: %d' % imageInfo.NEXT_IMG_START)

    rootHeader = genRootHeader(config, imageInfo, ImageInfo.TARGET_TYPE_FLASH)
    finalFlashHeader = rootHeader + b''.join(imageInfo.flashHeaders)
    finalFlashHeader = finalFlashHeader.ljust(4096, b'\x00')
    flashImage = finalFlashHeader
    for k in range(len(imageInfo.flashBins)):
        #print('k=%x\n',k)
        flashImage = flashImage.ljust(imageInfo.flashAddressStart[k], b'\x00')
        flashImage += imageInfo.flashBins[k]
    fileout = open(flash_file, 'wb')
    fileout.write(flashImage)
    fileout.close()

    xmodemRootHeader = genRootHeader(config, imageInfo, ImageInfo.TARGET_TYPE_XMODEM)
    xmodemImage = xmodemRootHeader + b''.join(imageInfo.xmodemHeaders)
    xmodemImage = xmodemImage.ljust(4096, b'\x00')
    for bin_data in imageInfo.xmodemBins:
        if len(bin_data)%128 != 0:
            bin_data += b'\0' * (128 - len(bin_data)%128)
        xmodemImage += bin_data
    fileout = open(xmodem_file, 'wb')
    fileout.write(xmodemImage)
    fileout.close()


if __name__ == '__main__':
    config_to_flash('ImageInfo.ini', 'flash.hex', 'xmodem.img')
    config_to_flash('FH8553_ImageInfo.ini', 'FH8553_flash.hex', 'FH8553_xmodem.img')