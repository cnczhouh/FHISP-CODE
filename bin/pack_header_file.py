#coding=utf-8
import zipfile
import os
import zlib
#import StringIO
import struct
import array
import sys
import platform

MAGIC_NUM = 'HDPK'

def get_file_path_info(f):
    lf = os.path.split(f)
    dn = lf[0]
    lf = os.path.splitext(lf[1])
    fn = lf[0]
    ext = lf[1].replace('.', '')
    return dn, fn, ext

def file_to_zipFile(fn):
    dname, fname, ext = get_file_path_info(fn)
    f = zipfile.ZipFile(fname+'.zip','w',zipfile.ZIP_DEFLATED)
    f.write(fn, arcname=fname+'.'+ext)
    f.close()
    return

'''
def file_to_zipData(fn):
    dname, fname, ext = get_file_path_info(fn)
    fio = StringIO.StringIO()
    f = zipfile.ZipFile(fio,'w', zipfile.ZIP_DEFLATED)
    f.write(fn, arcname=fname+'.'+ext)
    f.close()
    zipData = fio.getvalue()
    return zipData
'''
def file_to_zipData(fn):
    tmp_file = 'config_data.tmp'
    dname, fname, ext = get_file_path_info(fn)
    f = zipfile.ZipFile(tmp_file,'w',zipfile.ZIP_DEFLATED)
    f.write(fn, arcname=fname+'.'+ext)
    f.close()

    zipData = file_to_string(tmp_file)
    return zipData

def zlib_file_to_data(fn):
    f = open(fn, 'rb')
    data = f.read()
    f.close()
    result = zlib.compress(data, 9)
    print('compress from %d to %d'%(len(data), len(result)))
    return result

def magic_bytes():
    data = struct.pack('B', ord(MAGIC_NUM[0]))
    for i in range(1, len(MAGIC_NUM)):
        data += struct.pack('B', ord(MAGIC_NUM[i]))
    return data

def gen_header_info(dataSzie):
    return magic_bytes() + \
           struct.pack('I', dataSzie) +\
           struct.pack('I', dataSzie^0xffffffff) + \
           struct.pack('I', 0)

def is_data_pack_header(data):
    if (len(data) < 16):
        return False,0

    for i in range(len(MAGIC_NUM)):
        if (data[i] != MAGIC_NUM[i]):
            return False,0

    (dsize1, ) = struct.unpack('I', data[4:8])
    (dsize2, ) = struct.unpack('I', data[8:12])
    if (dsize1 != dsize2 ^ 0xffffffff):
        return False,0
    return True, dsize1


def is_pack_header_file(fn):
    f = open(fn, 'rb')
    data = f.read()
    f.close()
    result, = is_data_pack_header(data)
    return result


def file_to_array(fname):
    arr = array.array('B')
    f = open(fname, 'rb')
    arr.fromfile(f, os.path.getsize(fname))
    f.close()
    return arr

def file_to_string(fname):
    f = open(fname, 'rb')
    data = f.read()
    f.close()
    return data

def string_to_file(strData, fname):
    f = open(fname, 'wb')
    data = f.write(strData)
    f.close()
    return data

def array_to_file(arr, fname):
    f = open(fname, 'wb')
    arr.tofile(f)
    f.close()

def file_to_pack_header_file(fn):
    zd = file_to_zipData(fn)
    header = gen_header_info(len(zd)) + zd
    f = open('config_data.pk', 'wb')
    f.write(header)
    f.close()

def pack_file_to_other_file(fn, fother):
    zd = file_to_zipData(fn)
    header = gen_header_info(len(zd)) + zd
    fd = file_to_string(fother)
    string_to_file(fd+header, "RamBoot_Info.hex")
    print('pack from %s to %s, offset = 0x%08X,  compress size = %d'%(fn, fother, len(fd), len(header)))
'''
    arrOther = file_to_array(fother)
    for i in range(len(header)):
        if sys.version[0] < '3':
            d = ord(header[i])
        else:
            d = header[i]
        arrOther[offset+i] = d
    print('pack from %s to %s, offset = 0x%08X,  compress size = %d'%(fn, fother, offset, len(header)))
    array_to_file(arrOther, fother)
'''



def unpack_header_from_file(fn):
    print('unpack file = %s'%fn)
    d = file_to_string(fn)
    pos = d.find(MAGIC_NUM, 0)
    while(pos != -1):
        head = d[pos:pos+16]
        result, dsize = is_data_pack_header(head)
        pos += 16
        if (result):
            print('Find data, offset = 0x%08X, unpack to config.zip'%(pos-16))
            pdata = d[pos:pos+dsize]
            string_to_file(pdata, "config.zip")
            return True

        pos = d.find(MAGIC_NUM, pos)

    print('Find data error!')
    return False

def env_set():
    if (platform.system() == 'Windows'):
        os.system("color 0a")
    #curPath = os.path.split(os.path.realpath(__file__))[0]
    curPath = os.path.split(os.path.realpath(sys.argv[0]))[0]
    #curPath = os.path.dirname(sys.argv[0])
    os.chdir(curPath)
    #print "curPath : %s"%os.path.realpath(__file__)

if __name__ == '__main__':
    env_set()
    if (len(sys.argv) == 1):
        print('*********pack header file*********')
        pack_file_to_other_file('../ext/product_config.h', 'RamBoot_Firmware.hex')
    else:
        unpack_header_from_file(sys.argv[1])
        raw_input()
    pass