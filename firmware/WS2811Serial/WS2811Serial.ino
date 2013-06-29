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

boolean demo_mode = false;
uint_fast16_t dmx_address;


void setup() {
  strip.begin();
  strip.show(); // Initialize all pixels to 'off'
  
  // Configure the DIP switch pins to have pullups
  PORTD |= (1 << 5) + (1 << 6) + (1 << 7);
  PORTB |= (1 << 0);
  
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
  
  // Get DIP switch settings for DMX address
  dmx_address = (PIND >> 5) + ((PINB & 1) << 3);
  dmx_address = dmx_address ^ 0x0F;
  // Check for demo mode
  if (dmx_address == 0x0F) {
    demo_mode = true;
  }
}

void loop() {
  if (!demo_mode) {
    for (uint_fast16_t c = 0; c < NUM_LEDS; c++) {
        uint_fast16_t start = dmx_address*(NUM_LEDS*3) + c*3;
        setPixelColor(c, strip.Color(DMXSerial.read(start+1),DMXSerial.read(start+2), DMXSerial.read(start+3)));
    }
  }
  else {
     rainbow(50);
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

void rainbow(uint8_t wait) {
  uint16_t i, j;

  for(j=0; j<256; j++) {
    for(i=0; i< NUM_LEDS; i++) {
      setPixelColor(i, Wheel((i+j) & 255));
    }
    delay(wait);
  }
}

// Input a value 0 to 255 to get a color value.
// The colours are a transition r - g - b - back to r.
uint32_t Wheel(byte WheelPos) {
  if(WheelPos < 85) {
   return strip.Color(WheelPos * 3, 255 - WheelPos * 3, 0);
  } else if(WheelPos < 170) {
   WheelPos -= 85;
   return strip.Color(255 - WheelPos * 3, 0, WheelPos * 3);
  } else {
   WheelPos -= 170;
   return strip.Color(0, WheelPos * 3, 255 - WheelPos * 3);
  }
}
