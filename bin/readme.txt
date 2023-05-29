简介

	HeaderGen.py是由python写的一个脚本，用于生成DUOBAO各个镜像文件，需要python2.7或以上版本。
	工具会生成两个文件，Flash.img用于Flash烧写；xmodem.img用于xmodem协议发送。

使用方法
	
	1.建立一个ImageInfo.ini文件，填写镜像信息，格式如下：
		[productroot]
		MagicNumber=0xa4b7c9f8
		Product=0x4442414f
		Version=1

		[code1]
		Xmodem=Y
		FilePath=romboot_test.bin
		ImageName=Ramboot 
		FlashAddress=0x00001000
		MemoryAddress=0x10000000
		Entry=0x10000000
		Type=0x10

		[productroot]段里放入产品相关的属性，该段信息会放入最终镜像文件的头部
		
		Xmodem属性：
			Y 表示需要将当前section添加到xmodem.img中
			W 表示需要将当前section添加到xmodem.img中，同时需要写入到Flash

	2.将需要的bin文件放到和FilePath吻合的目录中

	3.双击HeaderGen.py，开始生成

其他
	
	生成的Flash.img将代码段按flash地址对齐合并在一起，其中头部做4096字节对齐。
	生成的xmodem.img将所有代码段合在一个文件中，方便发送。其中头的部分做128字节对齐，代码段之间也做128字节对齐



