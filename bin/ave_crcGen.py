import os
import struct
import configparser
import array
import random



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


infile = 'ave_stream.hex'
outfile = 'ave_stream_proc.hex'



def ave_crc_gen(infile, outfile):
    ave_stream_length = 1024-4
    ave_stream_num = 32

    binFile = open(infile, 'rb')
    fout = open(outfile, 'wb')

    binFile.seek(0,2)
    size = binFile.tell()
    binFile.seek(0,0)

    for i in range(ave_stream_num):
        ds = array.array('B')
        ds.fromfile(binFile, ave_stream_length)
        binFile.seek(4,1)
        crc = mycrc32(ds)
    #    print('crc: %x' % crc)
        ds.append(crc&0xff)
        ds.append((crc>>8)&0xff)
        ds.append((crc>>16)&0xff)
        ds.append((crc>>24)&0xff)
        ds.tofile(fout)

    binFile.close()
    fout.close()

if __name__ == '__main__':
    ave_crc_gen('ave_stream.hex', 'ave_stream_proc.hex')
    ave_crc_gen('FH8553_ave_stream.hex', 'FH8553_ave_stream_proc.hex')



