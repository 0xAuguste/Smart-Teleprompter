#include "TFT_eSPI.h"
#include "SPI.h"
#include "text.h"
TFT_eSPI tft;

int x = 10;

void setup() {
    tft.begin();
    tft.setRotation(3);
    tft.setTextSize(4);
    tft.setTextColor(TFT_BLACK);
    tft.fillScreen(TFT_WHITE);
}

void loop() {
    tft.drawString(text, x, 100);
    
    delay(20);
    tft.setTextColor(TFT_WHITE);
    tft.drawString(text, x, 100);

    x -= 8;
    tft.setTextColor(TFT_BLACK);
}
