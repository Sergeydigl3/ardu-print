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
static u8 Mil_Data[] = <codeblock>
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

