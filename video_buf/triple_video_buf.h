#ifndef TRIPLE_VIDEO_BUF_H
#define TRIPLE_VIDEO_BUF_H

#include "video_buf.h"

typedef struct tripleVideoBuf
{
    videoBuf_t *buf[3];
    videoBuf_t *in;   // 输入缓冲
    videoBuf_t *out;  // 输出缓冲
    videoBuf_t *temp; // 中间缓冲
} tripleVideoBuf_t;

/** tripleVideoBuf 初始化
 * input:   self tripleVideoBuf对象, videoBuf指针数组
 * output:  none
 */
void tripleVideoBuf_init(tripleVideoBuf_t *self, videoBuf_t *videoBuf[]);

/** 交换输入缓冲
 *      当输入缓冲写完毕时调用
 * input:   self tripleVideoBuf对象
 * output:  交换后的输入缓冲
 */
videoBuf_t *tripleVideoBuf_swapIn(tripleVideoBuf_t *self);

/** 获得最新的输出缓冲
 *      当输出缓冲读完毕时调用
 * input:   self tripleVideoBuf对象
 * output:  返回最新的输出缓冲
 */
videoBuf_t *tripleVideoBuf_swapOut(tripleVideoBuf_t *self);

#endif
