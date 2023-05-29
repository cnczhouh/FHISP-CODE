#!/bin/bash

OBJCOPY="arc-fullhan-elf32-objcopy"
projName="GuangChen_Firmware"

cd $(dirname $0)
echo $PWD

$OBJCOPY -O binary \
--change-section-address .drv_data-0x0 \
--change-section-address .osd_data-0x700000 \
$projName.elf $projName.hex

$OBJCOPY -O binary \
--only-section .entry_section \
--only-section .text \
--only-section .rodata \
--only-section .data \
$projName.elf firmware.hex

$OBJCOPY -O binary \
--only-section .drv_data \
$projName.elf drvRegInfo.hex

#python3 pad_to.py drvRegInfo_tmp.hex drvRegInfo.hex 0x5000
#rm drvRegInfo_tmp.hex

$OBJCOPY -O binary \
--only-section .osd_data \
$projName.elf osd_data.hex

python3 pack_header_file.py
python3 drvReg_crcGen.py
python3 ave_crcGen.py
#python3 data_combine.py
python3 firmware_headerGen.py
python3 makeFlash.py

