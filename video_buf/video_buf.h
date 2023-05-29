#ifndef VIDEO_BUFFER_H
#define VIDEO_BUFFER_H

typedef struct videoBuf
{
    unsigned char idx;
    int           width;
    int           height;
    int           frameCnt;
} videoBuf_t;

/** videoBuf 初始化
 * input:   self videoBuf对象, buffer编号idx(0~2), 存储图像的宽和高
 * output:  none
 */
void videoBuf_init(videoBuf_t *self, unsigned char idx, int width, int height);

/** 获取buffer编号(0~2)
 * input:   self videoBuf对象
 * output:  buffer编号
 */
unsigned char videoBuf_getAddressIdx(videoBuf_t *self);

/** 获取buffer中图像的宽度
 * input:   self videoBuf对象
 * output:  宽
 */
int videoBuf_getWidth(videoBuf_t *self);

/** 获取buffer中图像的高度
 * input:   self videoBuf对象
 * output:  高
 */
int videoBuf_getHeight(videoBuf_t *self);

/** 设置buffer中图像的宽高
 * input:   self videoBuf对象， 图像宽高
 * output:  none
 */
void videoBuf_setWidthHeight(videoBuf_t *self, int width, int height);

/** 获取指定缓冲中图像对应的时间戳，以帧为单位
 * input:   self videoBuf对象
 * output:  帧计数值
 */
int videoBuf_getFrameCnt(videoBuf_t *self);

/** 设置指定缓冲中图像对应的时间戳，以帧为单位
 * input:   self videoBuf对象， 帧计数值
 * output:  none
 */
void videoBuf_setFrameCnt(videoBuf_t *self, int frameCnt);

#endif
