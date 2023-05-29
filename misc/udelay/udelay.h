/**
 * udelay.h
 */
#ifndef _UDELAY_H_
#define _UDELAY_H_

#include "build.h"

#ifdef FIRMWARE_SOC_CLK
#define CPU_FREQ 90000000
#else
#define CPU_FREQ 45000000
#endif

#define LOOP_CYCLE 2

#define _1ms (CPU_FREQ / 1000 / LOOP_CYCLE)
#define _1us (CPU_FREQ / 1000 / 1000 / LOOP_CYCLE)

/** delay n microsecond */
void udelay(int n);

/** delay n millisecond */
void mdelay(int n);

#endif // !_UDELAY_H_