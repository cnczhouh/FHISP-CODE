#ifndef _DIRTY_INTERFACE_H_
#define _DIRTY_INTERFACE_H_

#include "product_config.h"
#include "drv_isp.h"
#include "drv_reg.h"
#include "fhprintf.h"

/**
 * 访问非OSD相关模块的数据，需通过此接口
 * 包括访问drvreg，isp非OSD模块，其他设备，flash等等
 * OSD内部模块将通过此模块对外进行访问
 */
void syncFontConfigWithDrvReg();
int  getOutputResolutionX();
int  getOutputResolutionY();
int  getOsdStartX();
int  getOsdStartY();

int  getIntt(void);

int  getOsdRefresh(void);
void setOsdRefresh(int mode);

int  getAutoExitTimer(void);
void setAutoExitTimer(int mode);
#endif  // !_DIRTY_INTERFACE_H_