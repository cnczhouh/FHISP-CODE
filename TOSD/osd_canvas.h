#ifndef _OSD_CANVAS_H_
#define _OSD_CANVAS_H_

#include "fh_types.h"

typedef struct _canvas {
    UINT8 *address;  // 画布起始地址
    UINT8 stride;   // 硬件配置水平字符数
    UINT8 width;    // 画布字符宽度
    UINT8 height;   // 画布字符高度
} canvas_t;

UINT8 *canvas_getAddress(canvas_t *this);
void canvas_setAddress(canvas_t *this, UINT8 *address);
int canvas_getStride(canvas_t *this);

#endif