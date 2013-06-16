#include <DMXSerial.h>
#include <Adafruit_NeoPixel.h>

// Parameter 1 = number of pixels in strip
// Parameter 2 = pin number (most are valid)
// Parameter 3 = pixel type flags, add together as needed:
//   NEO_RGB     Pixels are wired for RGB bitstream
//   NEO_GRB     Pixels are wired for GRB bitstream
//   NEO_KHZ400  400 KHz bitstream (e.g. FLORA pixels)
//   NEO_KHZ800  800 KHz bitstream (e.g. High Density LED strip)
Adafruit_NeoPixel strip = Adafruit_NeoPixel(2, 9, NEO_GRB + NEO_KHZ800);

#define NUM_LEDS 16

void setup() {
  strip.begin();
  strip.show(); // Initialize all pixels to 'off'
  
  colorWipe(strip.Color(255,0,0), 50);
  
  // Set the channel switching pins to outputs
  digitalWrite(A0, LOW);
  digitalWrite(A1,LOW);
  digitalWrite(A2,LOW);
  digitalWrite(A3,LOW);
  pinMode(A0, OUTPUT);
  pinMode(A1, OUTPUT);
  pinMode(A2, OUTPUT);
  pinMode(A3, OUTPUT);
  
  colorWipe(strip.Color(0,255,0), 50);
  
  // Set the differential transceiver to receive mode.
  digitalWrite(2, LOW);
  pinMode(2, OUTPUT);
  // Setup the DMX interrupts / parsing code.
  DMXSerial.init(DMXReceiver);
  
  colorWipe(strip.Color(0,0,255), 50);
  
  colorWipe(strip.Color(0,0,0), 50);
}

void loop() {
  // Some example procedures showing how to display to the pixels:
  for (uint8_t c = 0; c < NUM_LEDS; c++) {
      uint8_t start = c*3;
      setPixelColor(c, strip.Color(DMXSerial.read(start+1),DMXSerial.read(start+2), DMXSerial.read(start+3)));
  }
}

void setPixelColor(uint8_t pixel, uint32_t color) {
  // Change muxes to appropriate output
  setDualPixelColor(pixel, color, color);
}

void setDualPixelColor(uint8_t pixel, uint32_t color1, uint32_t color2) {
  // Change muxes to appropriate output
  PORTC = (PORTC & 0xF0) + (pixel & 0x0F);
  strip.setPixelColor(0, color1);
  strip.setPixelColor(1, color2);
  strip.show();
}

// Fill the dots one after the other with a color
void colorWipe(uint32_t c, uint8_t wait) {
  for(uint16_t i=0; i<NUM_LEDS; i++) {
      setPixelColor(i, c);
      delay(wait);
  }
}
