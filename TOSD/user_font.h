#ifndef _USER_FONT_H_
#define _USER_FONT_H_


extern unsigned char font_alnum[];

unsigned char get_alnum_char_index(unsigned char c);
void alnum_str_to_font_index(char *pData, unsigned char *pBuf);

#endif
