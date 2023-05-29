import os, sys, array
from time import strftime, localtime, time

ISP = ''
Type = 'Para'
input_file1 = 'flash.hex'
input_file2 = 'FH8553_flash.hex'
svn_file = 'svn_info.txt'
DATA_SVN_VERSION_LEN = 4
DATA_TIME_LEN = 4
DATA_SIZE_LEN = 4
FLASH_MAX_NUM = 100

DRV_FLASH_ADDR = 180*1024 #backup addr 0x45000

ADDR_OFFSET = 192

def get_svn_version(infile):
        fv = open(svn_file, 'r')
        for line in fv:
                if -1 != line.find('Revision'):
                        ver_string = line.split()[1]
                        version = int(ver_string,16)
                        return version
                
def get_sensor_name():
        current_path = sys.path[0]
        product_config_h = current_path[0: len(current_path) - 4] + '\ext\product_config.h'
        f1 = open(product_config_h, 'r')
        for line in f1:
                if -1 != line.find('#define '):
                        aline = line.split()
                        if aline[0] == '#define' and -1 != aline[1].find('E2PROM_'):
                                return aline[1][len('E2PROM_') : len(aline[1])]

def get_isp_name():
        current_path = sys.path[0]
        product_config_h = current_path[0: len(current_path) - 4] + '\ext\product_config.h'
        f1 = open(product_config_h, 'r')
        for line in f1:
                if -1 != line.find('#define '):
                        aline = line.split()
                        if aline[0] == '#define' and -1 != aline[1].find('GPIO_FUNC1'):
                                return 'FH8550D'
                        elif aline[0] == '#define' and -1 != aline[1].find('GPIO_FUNC2'):
                                return 'FH8550M'
                        elif aline[0] == '#define' and -1 != aline[1].find('GPIO_FUNC3'):
                                return 'FH8553'

def str2hex(string):
        hex_data = 0
        for i in range(len(string)):
                oct_data = int(string)
                x = (oct_data % pow(10, len(string) - i)) / pow(10, len(string) - i - 1)                
                hex_data = (hex_data << 4) + int(x)
        return hex_data      

def array_append(data_array,uint32,length):
        for i in range(length):
                data_array.append((uint32 >> (8 * i)) & 0xff)
        return data_array
        
if __name__ == '__main__':
        svn_version = get_svn_version(svn_file)
        str_svn_version = str(hex(svn_version))[2 :len(str(hex(svn_version)))]
        ISP_name = get_isp_name()
        sensor_name = get_sensor_name()
        str_current_time = strftime('%Y%m%d', localtime(time()))
        oct_current_time = str2hex(str_current_time)
        if ISP_name == 'FH8553':
                input_file = input_file2
        else:
                input_file = input_file1
                
        if os.path.exists(input_file) == False:
                print('File Not Finded:' + str(input_file))	
        flash_size = os.path.getsize(input_file)        
        print('Path = ' + sys.path[0])
        print('SVN Version: ' + str_svn_version)
        print('ISP: ' + ISP_name)
        print('Sensor: ' + sensor_name)
        print('Flash Size: ' + str(hex(flash_size)))
        print('Time: ' + str_current_time)        

        d8 = array.array('B')
        f1 = open(input_file, 'rb')
        f1.seek(0, 0)
        d8.fromfile(f1, DRV_FLASH_ADDR + ADDR_OFFSET)
        d8 = array_append(d8, svn_version, DATA_SVN_VERSION_LEN)
        d8 = array_append(d8, oct_current_time, DATA_TIME_LEN)
        d8 = array_append(d8, flash_size, DATA_TIME_LEN)

        offset = DRV_FLASH_ADDR + ADDR_OFFSET + DATA_SVN_VERSION_LEN + DATA_TIME_LEN + DATA_TIME_LEN
        f1.seek(offset, 0)
        d8.fromfile(f1, flash_size - offset)

        new_flash_head_path = ISP_name + '_' + sensor_name + '_' + 'Flash' + '_' + Type + '_R' + str_svn_version + '_' + str_current_time + '_' + 'XXX'

        for i in range(FLASH_MAX_NUM):
                if i == 0:
                        complete_path = new_flash_head_path + '.hex'
                else:
                        complete_path = new_flash_head_path + '_' + str(i+1) + '.hex'
                if os.path.exists(complete_path) == False:
                        f2 = open(complete_path, 'wb')
                        d8.tofile(f2)
                        f1.close()
                        f2.close()
                        break;
        if i < FLASH_MAX_NUM:
                print('Flash Name: ' + complete_path)
                os.system("explorer /select, %s"%complete_path)
        else:
                print('Same Solution Number Over The Limit: ' + str(FLASH_MAX_NUM))
