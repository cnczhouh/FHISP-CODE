/*****************************************************************************
*
*                                  OSD_driver.h
*
*	Copyright (c) 2013 Shanghai Fullhan Microelectronics Co., Ltd.
*						All Rights Reserved. Confidential.
*
*	File Description:
*		base function definition
*
*	Modification History:
*
******************************************************************************/
#ifndef _OSD_DRIVER_H_
#define _OSD_DRIVER_H_

#include <fh_types.h>

enum FONT_MODE {
    SIZE_16x16 = 0x5,
    SIZE_24x16 = 0x6,
    SIZE_24x24 = 0xA,
    SIZE_32x16 = 0x7,
    SIZE_32x24 = 0xB,
    SIZE_16x24 = 0x9,
    SIZE_16x32 = 0xD,
    SIZE_24x32 = 0xE,
    SIZE_32x32 = 0xF,
};

enum FONT_ROTATE {
    ROTATE_0 = 0,
    ROTATE_90,
    ROTATE_180,
    ROTATE_270,
};

void OSD_driver_SetFont(char *font);
void OSD_driver_SetStream(UINT8 *streams);
void OSD_driver_SetEnlargeEn(int hori, int vert);
void OSD_driver_SetTextStartXPos(UINT32 startX);
void OSD_driver_SetTextStartYPos(UINT32 startY);
void OSD_driver_SetTextWidth(UINT32 Width);
void OSD_driver_SetTextHeight(UINT32 Height);
void OSD_driver_SetColor(UINT32 color);
void OSD_driver_SetBackgroundColor(UINT32 color);
void OSD_driver_SetFontSize(UINT32 mode);
void OSD_driver_HighLightEnable(UINT32 enable);
void OSD_driver_SetHighLightPos(UINT32 startX, UINT32 startY, UINT32 endX, UINT32 endY);
void OSD_driver_SetHighLightColor(UINT32 color);
void OSD_driver_TextEdgeEnable(UINT32 enable);
void OSD_driver_SetEdgeColor(UINT32 color);
void OSD_driver_SetHighLightEdgeColor(UINT32 color);
void OSD_driver_SetHighLightBackgroundColor(UINT32 color);
void OSD_driver_HighLightEnable1(UINT32 enable);
void OSD_driver_SetHighLightPos1(UINT32 startX, UINT32 startY, UINT32 endX, UINT32 endY);
void OSD_driver_SetHighLightColor1(UINT32 color);
void OSD_driver_SetHighLightEdgeColor1(UINT32 color);
void OSD_driver_SetHighLightBkgColor1(UINT32 color);
void OSD_driver_Text_bypass(UINT32 enable);

#endif /*_OSD_DRIVER_H_*/
