#ifndef _USER_INTERFACE_H_
#define _USER_INTERFACE_H_


enum _OSD_RESERVED_CHAR {
    STREAM_END = 0,
    SPACE,
    NEWLINE,
    REPEAT,
    NOP,
    BLANK,
    BNL,
    RESERVED,

    NUM_0 = 8,
    NUM_1 = 9,
    NUM_2 = 10,
    NUM_3 = 11,
    NUM_4 = 12,
    NUM_5 = 13,
    NUM_6 = 14,
    NUM_7 = 15,
    NUM_8 = 16,
    NUM_9 = 17,

    _ENTER = 18,
    _UP,
    _RIGHT,
    _DOWN,
    _LEFT,
};

#define OSD_STRING_ADDR 0xA0015000
#define OSD_FONT_ADDR 0xc07c2000
#define FONT_BUF_SIZE (4 * 1024)  // 单个字库缓冲大小
#define MAX_STR_CNT (32)           // 一个页面最大字符串个数
#define MAX_STR_LEN (32)           // 字符串最大长度
#define STRING_BUF_SIZE (MAX_STR_CNT * MAX_STR_LEN)

char *getFontBuffer();
char *getString(int objIdxInMenu);
void choose_fontsize();
void loadFont();


#endif  // !_USER_INTERFACE_H_
