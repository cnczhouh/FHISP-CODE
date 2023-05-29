#ifndef _OSD_STREAM_H_
#define _OSD_STREAM_H_

/**
 * 显示缓冲 管理模块
 */

#define DISPLAY_BUF_COUNT 2
#define DISPLAY_BUF_SIZE 2048

unsigned char *getDisplayBuffer(int idx);

#endif
