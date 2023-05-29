/*****************************************************************************
*	Copyright (c) 2010-2017 Shanghai Fullhan Microelectronics Co., Ltd.
*						All Rights Reserved. Confidential.
******************************************************************************/
#ifndef _BUF_SWITCH_CFG_H
#define _BUF_SWITCH_CFG_H

#include "triple_video_buf.h"

extern tripleVideoBuf_t triple_video_buf;

void buf_init();
void buf_switchIpf();
void buf_switchIpb();

#endif
