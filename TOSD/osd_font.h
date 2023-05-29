#ifndef _OSD_CONFIG_H_
#define _OSD_CONFIG_H_

#include "fh_types.h"

typedef struct _font_config {
    UINT8 textEdgeEnable;
    UINT8 highLightEnable;
    UINT8 enlargeX;
    UINT8 enlargeY;
    UINT8 fontSize;

    UINT16 textColor;
    UINT16 edgeColor;
    UINT16 highlightColor;
    UINT16 highlightEdgeColor;
    UINT16 backgroundColor;
    UINT16 highlightBackgroundColor;
} font_config_t;

void initializeFontConfig();
void setFontConfigToHardware();
int getCharCountInRow(int pixelsInRow);
int getCharCountInColumn(int pixelsInColumn);
void useFontNumber(int x);  // TODO

#endif
