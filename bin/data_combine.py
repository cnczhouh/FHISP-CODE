import os
import array
import random

infile1 = 'drvRegInfoProc.hex'
binFile1 = open(infile1, 'rb')

infile2 = 'ave_stream_proc.hex'
binFile2 = open(infile2, 'rb')

infile3 = 'osd_data.hex'
binFile3 = open(infile3, 'rb')

outfile = 'data_combine_proc.hex'
fout = open(outfile, 'wb')

binFile1.seek(0,2)
size1 = binFile1.tell()
binFile1.seek(0,0)

ds = array.array('B')
ds.fromfile(binFile1, size1)

binFile2.seek(0,2)
size2 = binFile2.tell()
binFile2.seek(0,0)

ds.fromfile(binFile2, size2)

##############copy drv to default osd drv section################
binFile1.seek(0,0)
ds.fromfile(binFile1, size1)
#################################################################

binFile3.seek(0,2)
size3 = binFile3.tell()
binFile3.seek(0,0)

ds.fromfile(binFile3, size3)

ds.tofile(fout)

binFile1.close()
binFile2.close()
binFile3.close()

fout.close()




