/*============================================================================================
 *
 *  (C) 2010, Phyton
 *
 *  ť�񲰠�� ౮櫲 嬿 1986BE91 testboard
 *
 *  Š塏Π౥寱򠢫����J ƑӜ", 򮥮 鲪쿷鳥콭᪠౨�, ౨裠顮⬥丨򼍊 *  ௫��᳥퀬 𠧰᢮򪳠鵠౨쯦殨顤쿠౮��ﱮ⡍ilandr 1986BE91T1. ˮ� Phyton
 *  沠᫮顮򢥲񲢥񲨠蠠㯧� ௱즤񲢨��௫��ᮨ��䮬 鬨
 *  𠧰᢮򠭭冷 ௫��᳥즬 椮 ﲭ, Ў.
 *
 *--------------------------------------------------------------------------------------------
 *
 *  ՠꫠMain.c
 *
 *============================================================================================*/


#include <stdio.h>

#include "types.h"
#include "lcd.h"
#include "gl.h"
#include "text.h"
#include "1986be91_uart.h"

void EmblemFunc(void) {
	
		int pic_width = 128;
		int pic_height = 64;
		int pic_height_page = 8;
    u8 str;
    u32 chr;
    u32 let;
		int temp;
static u8 Mil_Data[] = {0x02, 0x7d, 0x82, 0x59, 0x26, 0x49, 0xb2, 0x05, 0xba, 0x41, 0xb6, 0xf9, 0xae, 0x75, 0xdf, 0x75, 0xdb, 0x7e, 0xd7, 0x7d, 0xd7, 0x7d, 0xd7, 0x7d, 0xd7, 0xfd, 0xb7, 0xdd, 0xf7, 0xdd, 0xff, 0xf5, 0xdf, 0xff, 0xf5, 0xff, 0xbf, 0xdb, 0x7f, 0xef, 0x7b, 0xdf, 0x7d, 0xd7, 0x3f, 0xdb, 0x6f, 0xbf, 0x6b, 0x9f, 0x37, 0x4b, 0xb5, 0x0f, 0x51, 0xa7, 0x12, 0xa5, 0x4b, 0x94, 0x2b, 0x45, 0x9a, 0x25, 0x5b, 0xa5, 0x0e, 0xb1, 0x4f, 0x92, 0x25, 0x5b, 0xa4, 0x53, 0x8c, 0x33, 0xc4, 0x29, 0x56, 0x89, 0x52, 0xad, 0x12, 0xed, 0x12, 0xed, 0x33, 0xce, 0xb5, 0x6a, 0x9d, 0xf2, 0xad, 0xd3, 0x25, 0xdf, 0x2b, 0xdf, 0x3f, 0xf7, 0xfd, 0xdf, 0xff, 0x75, 0xff, 0xdd, 0x77, 0xfd, 0xd7, 0xfd, 0xaf, 0x75, 0xff, 0x57, 0xfd, 0xdf, 0xf5, 0xbf, 0x6d, 0xfb, 0xdf, 0x75, 0xbf, 0xef, 0x7a, 0xdf, 0xf4, 0xdb, 0x01, 0x02, 0x04, 0x11, 0x02, 0x01, 0x04, 0x22, 0x01, 0xfe, 0xab, 0x56, 0xfd, 0xa7, 0x5d, 0xf7, 0xb9, 0x6f, 0xd6, 0x7d, 0xd7, 0xbd, 0xeb, 0xbf, 0xee, 0xbb, 0x6f, 0xbe, 0xeb, 0xdf, 0xb6, 0xfb, 0xaf, 0xfa, 0xbf, 0x6a, 0x9f, 0x75, 0x8f, 0x55, 0x2b, 0x94, 0x23, 0x4c, 0x93, 0x24, 0x53, 0x84, 0x59, 0x22, 0x49, 0xb6, 0x40, 0x15, 0xea, 0x00, 0xaa, 0x00, 0xaa, 0x04, 0x51, 0x04, 0x29, 0x82, 0x29, 0x84, 0x29, 0x52, 0x84, 0x19, 0xa2, 0x55, 0x0a, 0xd4, 0x21, 0x4e, 0x90, 0x2b, 0xd4, 0x22, 0x4d, 0x90, 0x25, 0x4a, 0x95, 0x2a, 0xd5, 0x2a, 0xdd, 0x23, 0xde, 0x75, 0x9e, 0xf5, 0x6b, 0xde, 0x75, 0xda, 0xb5, 0x6a, 0xc4, 0xbb, 0x45, 0x57, 0x9f, 0x7b, 0x5f, 0xff, 0xba, 0xff, 0xed, 0xff, 0xb5, 0xff, 0xdb, 0xf6, 0x5f, 0xf5, 0xdf, 0x7a, 0xef, 0xd5, 0x1f, 0xf7, 0xad, 0xf7, 0x5e, 0xfb, 0x00, 0x28, 0x10, 0x00, 0x24, 0x88, 0x10, 0x25, 0x08, 0xfb, 0x26, 0xdd, 0x33, 0xee, 0x55, 0xbb, 0x6d, 0xda, 0xb7, 0x5d, 0xb6, 0xcb, 0xf6, 0xad, 0xf6, 0x5d, 0xf7, 0x2d, 0xfe, 0x4b, 0x3e, 0x43, 0xbe, 0x03, 0x54, 0x2b, 0x84, 0x51, 0x2a, 0x04, 0x51, 0x08, 0x42, 0x91, 0x64, 0x98, 0x25, 0x8a, 0x21, 0xca, 0x55, 0xaa, 0xf1, 0xbe, 0x69, 0xd6, 0x29, 0x44, 0x90, 0x42, 0x00, 0x11, 0x84, 0x20, 0x02, 0x88, 0x22, 0x08, 0x42, 0x28, 0x82, 0x19, 0xa2, 0x54, 0x8b, 0x74, 0x81, 0x7e, 0x00, 0xf5, 0x0a, 0xb4, 0x41, 0x94, 0x29, 0x42, 0x94, 0x29, 0x46, 0x91, 0x2e, 0x51, 0xae, 0x5b, 0xb5, 0x6b, 0xbf, 0xd6, 0x7d, 0xeb, 0x5e, 0xb1, 0xef, 0x12, 0xed, 0x14, 0xe9, 0x56, 0xa1, 0x5e, 0x83, 0x3f, 0xcf, 0x3e, 0xfb, 0xff, 0xbf, 0xf5, 0xdf, 0xfd, 0xff, 0x55, 0xff, 0xb6, 0xfe, 0xad, 0xfb, 0xdb, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x57, 0xa8, 0x5b, 0xa6, 0xd9, 0xaf, 0x71, 0xdf, 0x64, 0xbf, 0xf5, 0xae, 0x7b, 0xce, 0x3b, 0x84, 0x2b, 0x85, 0x12, 0xa1, 0x04, 0x29, 0x82, 0x28, 0x01, 0x4a, 0x10, 0x82, 0x24, 0x09, 0xa0, 0x05, 0x50, 0xab, 0xd4, 0xbb, 0xe4, 0x1a, 0xe0, 0x1f, 0xf0, 0xaf, 0x55, 0xa2, 0x57, 0x25, 0x4a, 0x91, 0x2a, 0x84, 0x12, 0x40, 0x04, 0x20, 0x02, 0x80, 0x24, 0x00, 0x89, 0x20, 0x4a, 0x00, 0xb2, 0x45, 0x18, 0xe2, 0x0d, 0xb0, 0x4b, 0x94, 0x21, 0xd2, 0x04, 0x51, 0x84, 0x29, 0x82, 0x54, 0x09, 0xa2, 0x54, 0x09, 0x52, 0xa5, 0x5a, 0xa5, 0x5b, 0xf6, 0x5d, 0xa7, 0x7d, 0xdb, 0xb6, 0x6d, 0xb7, 0x48, 0xff, 0x00, 0xff, 0x80, 0x7f, 0xc0, 0x1d, 0xf2, 0x44, 0x19, 0xe2, 0x0b, 0xd7, 0x0b, 0x5f, 0xbf, 0x6f, 0xff, 0xfd, 0x7f, 0xfe, 0xdb, 0xff, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x20, 0x08, 0x12, 0x81, 0x6e, 0x15, 0xfa, 0xaf, 0x75, 0xdf, 0x75, 0xaf, 0xda, 0x2d, 0xd3, 0x2e, 0x40, 0x0a, 0x10, 0x40, 0x0a, 0x20, 0x00, 0x4a, 0x10, 0x82, 0x08, 0x21, 0x04, 0x40, 0x12, 0x00, 0x42, 0x08, 0x91, 0x26, 0x48, 0x97, 0x28, 0xd7, 0x08, 0x7f, 0x80, 0x3e, 0x23, 0x4c, 0xb5, 0x01, 0xaa, 0x00, 0x54, 0x00, 0x48, 0xa2, 0x00, 0x69, 0x10, 0xa4, 0x1a, 0xc0, 0x3e, 0xc0, 0x3d, 0xc2, 0x28, 0x03, 0xa8, 0x02, 0xa9, 0x12, 0xec, 0x5b, 0x25, 0x9a, 0x61, 0x8a, 0x14, 0xa1, 0x44, 0x0a, 0x51, 0x04, 0x52, 0xa5, 0x08, 0xb7, 0x68, 0x97, 0xfd, 0xb6, 0x6b, 0xdd, 0xab, 0x76, 0xdd, 0x2b, 0xdd, 0xb3, 0x4e, 0xb9, 0x46, 0xb9, 0xc6, 0x79, 0xc6, 0xf9, 0xe6, 0xb9, 0xf2, 0x6c, 0xda, 0xf9, 0x5e, 0xf9, 0x5c, 0xfa, 0xbd, 0xdd, 0xfd, 0xbd, 0x75, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x01, 0x02, 0x05, 0x85, 0x2f, 0x15, 0xda, 0x25, 0xda, 0xa2, 0x54, 0x90, 0x61, 0x84, 0x40, 0x10, 0x05, 0x40, 0x12, 0x00, 0x44, 0x10, 0x81, 0x04, 0x20, 0x09, 0x00, 0x45, 0x10, 0x42, 0x90, 0x25, 0xc0, 0x2a, 0x90, 0x65, 0x90, 0xf0, 0x25, 0xf0, 0xa2, 0x50, 0x00, 0x42, 0x08, 0x81, 0x0a, 0x21, 0x04, 0x92, 0x01, 0x2c, 0x50, 0x8d, 0x7f, 0x93, 0x7c, 0x03, 0x58, 0x22, 0x89, 0x20, 0x8a, 0x20, 0x5f, 0x00, 0x29, 0x82, 0x74, 0x8b, 0xb4, 0x09, 0x02, 0x54, 0x00, 0xa5, 0x5a, 0x01, 0xfc, 0x01, 0xfe, 0x01, 0xfe, 0x52, 0xad, 0xfb, 0xa6, 0xdd, 0xf2, 0xed, 0x7b, 0xfc, 0xfe, 0xef, 0x7d, 0xff, 0xf7, 0xfd, 0xdf, 0xff, 0xf6, 0x7f, 0xf5, 0xbf, 0xf7, 0xdd, 0xef, 0xbd, 0x77, 0x7f, 0xd5, 0x7f, 0xf6, 0x5d, 0xf7, 0xbd, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x80, 0x20, 0x48, 0x92, 0x04, 0xa9, 0x00, 0x82, 0x28, 0x81, 0x2a, 0x83, 0x26, 0x4d, 0x9a, 0x67, 0x9d, 0x37, 0xdc, 0x3d, 0xd4, 0x3a, 0xd8, 0xb4, 0x60, 0x51, 0xe4, 0x90, 0x61, 0xc4, 0x4b, 0xb4, 0x83, 0x54, 0x03, 0x94, 0x2b, 0x96, 0x3d, 0xe9, 0x12, 0xad, 0x10, 0x05, 0x51, 0x04, 0x00, 0x10, 0x42, 0x00, 0x10, 0x84, 0x01, 0x28, 0x82, 0x15, 0x24, 0x49, 0xb8, 0x42, 0xa8, 0x52, 0xc0, 0x94, 0x21, 0xcd, 0x12, 0x28, 0x40, 0x07, 0xa8, 0x02, 0x50, 0x05, 0x40, 0x12, 0x44, 0x89, 0x12, 0xa4, 0x49, 0xd6, 0x71, 0xfe, 0xdb, 0x7e, 0xfd, 0xbf, 0xff, 0xee, 0x7f, 0xff, 0x77, 0xff, 0xfb, 0xbf, 0xff, 0xff, 0x6f, 0xfd, 0xbf, 0xff, 0xf7, 0xbf, 0xfb, 0xdf, 0xff, 0x6a, 0xff, 0x80, 0x7f, 0x80, 0x6d, 0x93, 0x25, 0xdb, 0x23, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x80, 0x20, 0x50, 0x84, 0x29, 0x12, 0x44, 0x91, 0x24, 0x88, 0x22, 0x88, 0x20, 0x4a, 0x94, 0x22, 0x54, 0x89, 0x36, 0xc0, 0x1e, 0xe1, 0x1e, 0xa0, 0x5f, 0xa0, 0x5f, 0xa0, 0x5f, 0xa9, 0x56, 0xed, 0x12, 0xed, 0x5b, 0xb5, 0x4e, 0xfb, 0x55, 0xaf, 0xfa, 0xad, 0x5b, 0xf6, 0xad, 0xdb, 0x75, 0xdf, 0xb5, 0x6e, 0xd5, 0xba, 0xec, 0x38, 0xe9, 0xb0, 0x54, 0xf0, 0xd2, 0xa0, 0xf4, 0xa1, 0x68, 0xd2, 0xb4, 0xd1, 0x7a, 0xd4, 0xf9, 0x5a, 0xf4, 0xb9, 0xec, 0xf9, 0xac, 0xfa, 0x74, 0xdd, 0x7a, 0xed, 0xbe, 0xeb, 0xfe, 0xb7, 0xfd, 0xaf, 0xfb, 0xdd, 0xff, 0x55, 0xff, 0xeb, 0xbe, 0xfd, 0xd7, 0x7d, 0xff, 0xd5, 0x7f, 0xee, 0xbb, 0xfe, 0xd7, 0x7f, 0xfd, 0xd7, 0x7e, 0xf7, 0xbd, 0xef, 0xfe, 0xdb, 0xff, 0xdb, 0xfe, 0xdb, 0x7f, 0xf6, 0x5d, 0xa2, 0x5c, 0xa3};
    LCD_CLS();
    let = 0;
     //0
		SetCrystal(LCD_CRYSTAL1);
		for (str=0; str<8;str++)
        {
				
        LCD_SET_PAGE(str);
				
				temp = str*128;
        for (chr=0;chr<64;chr++)
				{
					LCD_SET_ADDRESS(chr);
					WriteLCD_Data(Mil_Data[temp+chr]);
				}			
		}
		SetCrystal(LCD_CRYSTAL2);
		for (str=0; str<8;str++)
			{
        LCD_SET_PAGE(str);
				temp = str*128;
        for (chr=64;chr<128;chr++)
				{
					LCD_SET_ADDRESS(chr);
					WriteLCD_Data(Mil_Data[temp+chr]);
				}			
		}
			

	}
//    for (str=1;str<6;str++)
//        {
//        LCD_SET_PAGE(str);
//        for (chr=8;chr<38;chr++)
//                {
//                LCD_SET_ADDRESS(chr);
//                WriteLCD_Data(Mil_Data[let++]);
//                }
//        }
//			}
   /* SetCrystal(LCD_CRYSTAL2); //1
    for (str=1;str<4;str++)
        {
        LCD_SET_PAGE(str);
        for (chr=0;chr<56;chr++)
                {
                LCD_SET_ADDRESS(chr);
                WriteLCD_Data(Mil_Data[let++]);
                }
        }
}*/



int main(void) {
	uc8 a[7] = "Hello,";
	uc8 b[8] = "My Dog!";
	 LCD_INIT();
//	LCD_CLS();
  EmblemFunc();
	
	//LCD_PUTS(67,8, &a[0]);
	//LCD_PUTS(67,20, &b[0]);
}

/*============================================================================================
 * ˮ ��ࡍain.c
 *============================================================================================*/

