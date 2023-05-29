import os
import struct
import configparser
import array

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


def genFlashImgHeader(config, section, imageInfo):
    if section[0:4] == 'code':
        imageInfo.imgc_flash += 1
    elif section[0:5] == 'param':
        imageInfo.paramc_flash += 1
    else:
        print('non section:')
        return
    
#    isXmodem = False
#    if config.has_option(section, 'Xmodem'):
#        isXmodem = True
#        if section[0:4] == 'code':
#            imageInfo.imgc_xmodem += 1
#        elif section[0:5] == 'param':
#            imageInfo.paramc_xmodem += 1
#        if config.get(section, 'Xmodem') == 'W':
#            imageInfo.XMODEM_TO_FLASH = True
#            print('xmodem image(write to flash):')
#        else:
#            print('xmodem image:')

    filePath = config.get(section, 'FilePath')
    imageSize = os.path.getsize(filePath)
    imageSizePacked = struct.pack('I', imageSize)
    
    imageName = config.get(section, 'ImageName')
    if imageName == 'firmware':
        print("the image is firmware!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
    else:
        imageInfo.imgc_flash -= 1
        return
    print('%s, size: 0x%x' % (imageName, imageSize))

    filePath = config.get(section, 'FilePath')
    imageSize = os.path.getsize(filePath)
    imageSizePacked = struct.pack('I', imageSize)
    binFile = open(filePath, 'rb')
    binData = binFile.read()
    binFile.close()

    imageInfo.flashBins.append(binData)

    imageName = imageName.ljust(32, '\0')
    imageName = imageName.encode('utf-8')

    flashAddr = config.get(section, 'FlashAddress')
    if not flashAddr:
        print('FlashAddress is empty, put it at 0x%08x' % imageInfo.NEXT_IMG_START)
        flashAddrInt = imageInfo.NEXT_IMG_START
    else:
        flashAddrInt = int(flashAddr, 16)
        if flashAddrInt < imageInfo.NEXT_IMG_START:
            print("Flash Address at %s has been taken, put it at 0x%08x" % \
                  (flashAddr, imageInfo.NEXT_IMG_START))
            flashAddrInt = imageInfo.NEXT_IMG_START

    #flash ADDR = flashAddrInt + sizeof(image_header)
    flashAddrInt += 64
            
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

    crc = mycrc32(binData)
    print('crc: %x' % crc)
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

    imageInfo.flashHeaders.append(imageHeader)
    

config = configparser.ConfigParser()
config.read('ImageInfo.ini')

imageInfo = ImageInfo()

outfile = 'firmware_bak.hex'  #backup firmware
fout = open(outfile, 'wb')

for section in config.sections():
    genFlashImgHeader(config, section, imageInfo)
  
   

imageInfo.NEXT_IMG_START = 64 * (imageInfo.imgc_flash + imageInfo.paramc_flash)
print('HeaderSize: %d' % imageInfo.NEXT_IMG_START)

finalFlashHeader = b''.join(imageInfo.flashHeaders)
#finalFlashHeader = finalFlashHeader.ljust(4096, b'\x00')
flashImage = finalFlashHeader
for k in range(len(imageInfo.flashBins)):
#    flashImage = flashImage.ljust(64, b'\x00')
    flashImage += imageInfo.flashBins[k]

fileout = open('firmware.hex', 'wb')
fileout.write(flashImage)
fileout.close()

##################################################################################
#############################backup firmware####################################
flash_fir_addr = 0x80000
flash_bak_addr = 0x5000

infile = 'firmware.hex'
fin = open(infile, 'rb')


fin.seek(0,2)
size = fin.tell()
fin.seek(0,0)

ds = array.array('B')
ds.fromfile(fin, size)

ds[36]=((flash_bak_addr+64)&0xff)
ds[37]=(((flash_bak_addr+64)>>8)&0xff)
ds[38]=(((flash_bak_addr+64)>>16)&0xff)
ds[39]=(((flash_bak_addr+64)>>24)&0xff)

ds.tofile(fout)

fin.close()
fout.close()
