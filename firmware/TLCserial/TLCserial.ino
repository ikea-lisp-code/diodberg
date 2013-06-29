#include <DMXSerial.h>

/*
    Basic Pin setup:
    ------------                                  ---u----
    ARDUINO   13|-> SCLK (pin 25)           OUT1 |1     28| OUT channel 0
              12|                           OUT2 |2     27|-> GND (VPRG)
              11|-> SIN (pin 26)            OUT3 |3     26|-> SIN (pin 11)
              10|-> BLANK (pin 23)          OUT4 |4     25|-> SCLK (pin 13)
               9|-> XLAT (pin 24)             .  |5     24|-> XLAT (pin 9)
               8|                             .  |6     23|-> BLANK (pin 10)
               7|                             .  |7     22|-> GND
               6|                             .  |8     21|-> VCC (+5V)
               5|                             .  |9     20|-> 2K Resistor -> GND
               4|                             .  |10    19|-> +5V (DCPRG)
               3|-> GSCLK (pin 18)            .  |11    18|-> GSCLK (pin 3)
               2|                             .  |12    17|-> SOUT
               1|                             .  |13    16|-> XERR
               0|                           OUT14|14    15| OUT channel 15
    ------------                                  --------

    -  Put the longer leg (anode) of the LEDs in the +5V and the shorter leg
         (cathode) in OUT(0-15).
    -  +5V from Arduino -> TLC pin 21 and 19     (VCC and DCPRG)
    -  GND from Arduino -> TLC pin 22 and 27     (GND and VPRG)
    -  digital 3        -> TLC pin 18            (GSCLK)
    -  digital 9        -> TLC pin 24            (XLAT)
    -  digital 10       -> TLC pin 23            (BLANK)
    -  digital 11       -> TLC pin 26            (SIN)
    -  digital 13       -> TLC pin 25            (SCLK)
    -  The 2K resistor between TLC pin 20 and GND will let ~20mA through each
       LED.  To be precise, it's I = 39.06 / R (in ohms).  This doesn't depend
       on the LED driving voltage.
    - (Optional): put a pull-up resistor (~10k) between +5V and BLANK so that
                  all the LEDs will turn off when the Arduino is reset.

    If you are daisy-chaining more than one TLC, connect the SOUT of the first
    TLC to the SIN of the next.  All the other pins should just be connected
    together:
        BLANK on Arduino -> BLANK of TLC1 -> BLANK of TLC2 -> ...
        XLAT on Arduino  -> XLAT of TLC1  -> XLAT of TLC2  -> ...
    The one exception is that each TLC needs it's own resistor between pin 20
    and GND.

    This library uses the PWM output ability of digital pins 3, 9, 10, and 11.
    Do not use analogWrite(...) on these pins.

    This sketch does the Knight Rider strobe across a line of LEDs.

    Alex Leone <acleone ~AT~ gmail.com>, 2009-02-03 */

#include "Tlc5940.h"
#define NUM_LEDS 16

static int bright[3] = {0, 1224, 2650};
boolean demo_mode = false;
uint_fast16_t dmx_address;

void setup()
{
  /* Call Tlc.init() to setup the tlc.
     You can optionally pass an initial PWM value (0 - 4095) for all channels.*/
  Tlc.init();
  Tlc.set(0, 4095);
  Tlc.update();
  delay(500);
  
  // Configure the DIP switch pins to have pullups
  PORTC |= (1 << 0) + (1 << 1) + (1 << 2) + (1 << 3);
  
  // Set the differential transceiver to receive mode.
  digitalWrite(2, LOW);
  pinMode(2, OUTPUT);
  
  // Setup the DMX interrupts / parsing code.
  DMXSerial.init(DMXReceiver);
  Tlc.set(1, 4095);
  Tlc.update();
  delay(500);
  
  // Get the preset dmx address from DIP switch
  uint8_t dip_value = PINC & 0x0F;
  dmx_address = (dip_value >> 3) + ((dip_value >> 1) & 0x02) +
      ((dip_value << 1) & 0x04) + ((dip_value << 3) & 0x08);
  dmx_address = dmx_address ^ 0x0F;
  // Check for demo mode.
  if (dmx_address == 0x0F) {
    demo_mode = true;
  }
  
  // Chill out.
  delay(500);
  Tlc.set(2, 4095);
  Tlc.update();
}

void loop()
{
   if (!demo_mode) {
     for (uint_fast16_t i = 0; i < 48; i++) {
       Tlc.set(i, DMXSerial.read(i + 1 + dmx_address*NUM_LEDS*3) << 4);
     }

   }
   else {
     demo_mode_lights();
   }
}

void demo_mode_lights() {
  for (int i = 0; i < 9; i++) {
    Tlc.set(i*3, 4095);
  }
  Tlc.update();
  delay(500);
  
  for (int i = 0; i < 9; i++) {
    Tlc.set(i*3+2, 0);
  }
  Tlc.update();
  delay(500);
  
  for (int i = 0; i < 9; i++) {
    Tlc.set(i*3+1, 4095);
  }
  Tlc.update();
  delay(500);
  
  for (int i = 0; i < 9; i++) {
    Tlc.set(i*3, 0);
  }
  Tlc.update();
  delay(500);
  
  for (int i = 0; i < 9; i++) {
    Tlc.set(i*3+2, 4095);
  }
  Tlc.update();
  delay(500);
  
  for (int i = 0; i < 9; i++) {
    Tlc.set(i*3+1, 0);
  }
  Tlc.update();
  delay(500);
}
