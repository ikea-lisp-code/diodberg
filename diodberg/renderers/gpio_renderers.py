from diodberg.core.renderer import Renderer
try:
    import RPi.GPIO
except ImportError as err: 
    sys.stderr.write("Error: failed to import module ({})".format(err))


class PiGPIORenderer(Renderer):
    """ PiGPIORenderer provides a renderer interface directly to the GPIO pins on
    the RaspberryPi. It assumes that all the pixels on a panel here are on the
    same universe. The GPIO is configured to reflect the pin outs on the board.
    """ 
    
    __num_channels = 26
    __pwm_frequencyHz = 50
    __pwm_init_dc = 0

    def __init__(self, channels = 26):
        super(PiGPIORenderer, self).__init__()
        RPi.GPIO.setmode(RPi.GPIO.BOARD)
        RPi.GPIO.setwarnings(True)
        self.__pwm = []
        for channel in xrange(channels):
            RPi.GPIO.setup(channel, RPi.GPIO.OUT, initial = RPi.GPIO.LOW)
            self.__pwm.append(RPi.GPIO.PWM(channel, PiGPIORenderer.__pwm_frequencyHz))
            self.__pwm[channel].start(PiGPIORenderer.__pwm_init_dc)
        
    def render(self, panel):
        for loc, pixel in panel.iteritems():
            assert pixel.address.universe is 0, "All pixels on universe 0."
            address = pixel.address.address
            norm = 255.
            self.__pwm[address].ChangeDutyCycle(pixel.color.red/norm)
            self.__pwm[address + 1].ChangeDutyCycle(pixel.color.green/norm)
            self.__pwm[address + 2].ChangeDutyCycle(pixel.color.blue/norm)

    def __del__(self):
        for pwm_channel in self.__pwm:
            pwm_channel.stop()
        RPi.GPIO.cleanup()

    def __repr__(self):
        return "PiGPIORenderer"


class PiToWS2812Renderer(Renderer):
    """ PiToWS2812Renderer provides a renderer interface directly to the WS2812
    board using the GPIO pins on the RaspberryPi. The serial protocol here is 
    described in this hilarious datasheet:
    http://partfusion.com/wp-uploads/2013/01/WS2812preliminary.pdf
    """ 
    
    __num_channels = 26
    __bit_width = 24
    __sleep_resetS = 55e-6
    __sleep_T0HS = 0.35e-6
    __sleep_T1HS = 0.70e-6
    __sleep_T0LS = 0.80e-6
    __sleep_T1LS = 0.60e-6

    def __init__(self, channels):
        super(PiToWS2812Renderer, self).__init__()
        RPi.GPIO.setmode(RPi.GPIO.BOARD)
        RPi.GPIO.setwarnings(True)
        assert len(channels) > 0, "Empty number of GPIO pins from RPi." 
        for channel in channels:
            RPi.GPIO.setup(channel, RPi.GPIO.OUT, initial = RPi.GPIO.LOW)            
        
    def render(self, panel):
        for loc, pixel in panel.iteritems():
            assert pixel.address.universe is 0, "All pixels on universe 0."
            channel = pixel.address.address
            data = pixel.color.green << 16 | pixel.color.red << 8 | pixel.color.blue
            for i in xrange(PiToWS2812Renderer.__bit_width, -1, -1):
                if data & (1 << i):
                    RPi.GPIO.output(channel, RPi.GPIO.HIGH)
                    time.sleep(PiToWS2812Renderer.__sleep_T1HS)
                    RPi.GPIO.output(channel, RPi.GPIO.LOW)
                    time.sleep(PiToWS2812Renderer.__sleep_T1LS)
                else:
                    RPi.GPIO.output(channel, RPi.GPIO.HIGH)
                    time.sleep(PiToWS2812Renderer.__sleep_T0HS)
                    RPi.GPIO.output(channel, RPi.GPIO.LOW)
                    time.sleep(PiToWS2812Renderer.__sleep_T0LS)
            time.sleep(PiToWS2812Renderer.__sleep_resetS)

    def __del__(self):
        RPi.GPIO.cleanup()

    def __repr__(self):
        return "PiToWS2812Renderer"
