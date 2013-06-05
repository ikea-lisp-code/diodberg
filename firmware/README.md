# diodberg device firmware

## Platform

The diodberg LED driver hardware is a arduino-mini-based design that drives two chained TLC5947 LED driver chips.

Control input is delivered as DMX over ethernet. There is a differential transceiver that decodes the ethernet line signal and converts it to a 5V serial input to the ATMega 168. A 4-switch DIP switch is present to set the starting address for the board.

Each board can drive at most 16 RGB LED holds (48 TLC channels).

## Code

The current firmware is really simple. It simply continuously sets each TLC5947 LED channel to the last recorded value of the associated DMX channel. DMX information is monitored using serial RX interrupts.

### Required Libraries

* TLC (https://code.google.com/p/tlc5940arduino/)
* DMXSerial (http://www.mathertel.de/Arduino/DMXSerial.aspx)

# Questions? 

Email <chris@notspelledright.com>, <yuanyu.chen@gmail.com>.
