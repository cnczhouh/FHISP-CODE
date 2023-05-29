import os
import struct
import configparser
import array
import random

drv_reg_com_length = 0x40
drv_reg_para_length = 2880
drv_reg_group_length = 0x1000
drv_reg_group_num = 5

drv_reg_gamma_offset = 0x500
drv_reg_gamma_size = 288*4

drv_reg_gamma_table_size = 3584


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


def int2File(fp, val):
    dataArr = array.array('B')
    dataArr.append(val&0xff)
    dataArr.append((val>>8)&0xff)
    dataArr.append((val>>16)&0xff)
    dataArr.append((val>>24)&0xff)
    dataArr.tofile(fp)


infile = 'drvRegInfo.hex'
binFile = open(infile, 'rb')

outfile = 'drvRegInfoProc.hex'
fout = open(outfile, 'wb')

binFile.seek(0,2)
size = binFile.tell()
binFile.seek(0,0)

ds = array.array('B')
ds.fromfile(binFile, drv_reg_com_length)
crc = mycrc32(ds)
#print('crc: %x' % crc)

int2File(fout, drv_reg_com_length)
int2File(fout, crc)

ds.fromfile(binFile, drv_reg_group_length-drv_reg_com_length-8)
ds.tofile(fout)

for i in range(drv_reg_group_num-1):
    binFile.seek(8, 1)
    ds = array.array('B')
    ds.fromfile(binFile, drv_reg_para_length)
    crc = mycrc32(ds)

    int2File(fout, drv_reg_para_length)
    int2File(fout, crc)
#    print('crc: %x' % crc)
    ds.fromfile(binFile, drv_reg_group_length-drv_reg_para_length-8)
    ds.tofile(fout)




for i in range(4):
    binFile.seek(8, 1)
    ds = array.array('B')
    ds.fromfile(binFile, drv_reg_gamma_table_size)
    crc = mycrc32(ds)

    int2File(fout, drv_reg_gamma_table_size)
    int2File(fout, crc)
#    print('crc: %x' % crc)
    ds.fromfile(binFile, drv_reg_group_length-drv_reg_gamma_table_size-8)
    ds.tofile(fout)

binFile.close()

fout.close()




