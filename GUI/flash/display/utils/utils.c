#include "../user/lcd.h"
#include "../user/gl.h"
//#include "joystick.h"

void LCD_PutPixel(u32 x, u32 y) {
    u32 shifted, page;
    u8 data;

    if ((x>MAX_X)|(y>MAX_Y)) return;

    SetCrystal((LCD_Crystal)(x/64));
    x %= 64;

    page = y/8;
    shifted = (1 << (y%8));
    LCD_SET_PAGE(page);
    LCD_SET_ADDRESS(x);
    data = ReadLCD_Data();
    switch (CurrentMethod){
        case MET_OR :   data |= shifted;    break;
        case MET_XOR :  data ^= shifted;    break;
    }
    LCD_SET_ADDRESS(x);
    WriteLCD_Data(data);
}