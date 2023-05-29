#ifndef _OSD_SCREEN_H_
#define _OSD_SCREEN_H_

#include "osd_canvas.h"

typedef struct _osd_screen {
    UINT8 *  address;  // 屏幕首地址
    canvas_t canvas;  // 屏幕对应画布
    UINT8    stride;   // 每行所占字节数
    UINT8    width;
    UINT8    height;
} screen_t;

void screen_setAddress(UINT8 *address);
UINT8 *screen_getAddress();
void screen_setWidth(int width);
void screen_setHeight(int height);
void      screen_updateCanvas();
canvas_t *screen_getCanvas();
void      screen_initilize();
void      screen_clean();
void      screen_swapBuffer();
void      screen_cleanCurrent();

unsigned char *screen_getCurrBuf(int x, int y);

#endif  // !_OSD_SCREEN_H_