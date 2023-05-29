echo %~dp0
echo %cd%

set projName=Guangchen_Firmware

copy %cd%\Release\%projName%.map  %~dp0 /Y
copy %cd%\Release\%projName%.elf  %~dp0 /Y
::copy %cd%\..\Release\%projName%.hex  %~dp0 /Y
cd %~dp0

elfdump -T -t %projName%.elf -o %projName%.txt
::elf2hex -B -p 0x0  %projName%.elf
elf2hex -B -p .text:0x0  -p .drv_reg_com:0x50000  -p .osd_streams:0x59000  %projName%.elf

hexSplit.py
pack_header_file.py
drvReg_crcGen.py
ave_crcGen.py
data_combine.py
firmware_headerGen.py
makeFlash.py

FH8553_hexSplit.PY
pack_header_file.py
FH8553_ave_crcGen.py
FH8553_data_combine.py
FH8553_firmware_headerGen.py
FH8553_makeFlash.py


pause
