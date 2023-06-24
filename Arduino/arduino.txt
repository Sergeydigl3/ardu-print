#include <SPFD5408_Adafruit_GFX.h>
#include <SPFD5408_Adafruit_TFTLCD.h>

// Assign human-readable names to some common 16-bit color values:
#define BLACK   0x0000
#define BLUE    0x001F
#define RED     0xF800
#define GREEN   0x07E0
#define CYAN    0x07FF
#define MAGENTA 0xF81F
#define YELLOW  0xFFE0
#define WHITE   0xFFFF


// Initialize the TFT display
#define LCD_CS A3
#define LCD_CD A2
#define LCD_WR A1
#define LCD_RD A0
#define LCD_RESET A4
Adafruit_TFTLCD tft(LCD_CS, LCD_CD, LCD_WR, LCD_RD, LCD_RESET);


boolean first = true;
// Initialize the buffer for storing incoming UART data



void setup()
{
  // Initialize the serial port
  Serial.begin(200000);

  // Initialize the TFT display
  tft.reset();
  tft.begin(0x9341);
  tft.setRotation(0);
  Serial.println("TFT initialized");
  tft.setAddrWindow(0, 0, tft.width() - 1, tft.height() - 1);
  // Send to serial width and height
  Serial.print("Width: ");
  Serial.println(tft.width());
  Serial.print("Height: ");
  Serial.println(tft.height());
  tft.fillScreen(RED);

  // lcd buffer fill BLUE
  tft.pushColorsSerialStart(true);

}


void loop()
{
  // Check if there is any data available on the serial port

  if (Serial.available() > 1)
  {
    byte first_byte_color = Serial.read();
    byte second_byte_color = Serial.read();

    // Serial.println("Rodger that");


    // tft.pushColorsSerialStart(false);

    tft.pushColorsSerialSend(first_byte_color, second_byte_color);
      // if (i%1000 == 0) Serial.println("Ya durak 0");
    
    // tft.pushColorsSerialEnd();

  }
}