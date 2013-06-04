import array
import pygame
import sys
import time
from diodberg.core.types import Color
# Protocol-specific imports
try:
    from ola.ClientWrapper import ClientWrapper
    import RPi.GPIO
    import serial
except ImportError as err: 
    sys.stderr.write("Error: failed to import module ({})".format(err))


class Renderer(object):
    """ Renderer is an abstract base class for objects that actually render pixels
    that have been filled in.
    """ 

    def __init__(self, universes = 1):
        pass
    
    def render(self, panel):
        """Perform a rendering action for an actual Panel. Subclass this method for a
        new renderer.
        """
        pass

    def __repr__(self):
        pass


class DMXRenderer(Renderer):
    """ DMXRenderer provides a renderer interface to the OLA client. You should
    specify the number of DMX universes panel pixels are spread over.
    """
    
    __dmx_buffer_size = 512
    __default_channel_val = 0
    
    def __init__(self, universes = 1):
        super(DMXRenderer, self).__init__()
        # Initialize a shared storage buffer
        default_buffer = [DMXRenderer.__default_channel_val]*DMXRenderer.__dmx_buffer_size
        self.__buffer = {}
        for i in xrange(universes):
            self.__buffer[i] = array.array('B', default_buffer)
        self.__wrapper = ClientWrapper()
        self.__client = self.__wrapper.Client()

    def render(self, panel):
        # Fill in the buffer.
        for loc, pixel in panel.items():
            if pixel.live:
                universe = pixel.address.universe
                address = pixel.address.address
                self.__buffer[universe][address] = pixel.color.red
                self.__buffer[universe][address + 1] = pixel.color.green
                self.__buffer[universe][address + 2] = pixel.color.blue
        # Send the buffer over DMX.
        for universe, buf in self.__buffer.iteritems():
            self.__client.SendDmx(universe, buf, self.__dmx_sent)
            self.__wrapper.Run()
        
    def __dmx_sent(self):
        self.__wrapper.Stop()

    def __repr__(self):
        return "DMXRenderer"


class DMXSerialRenderer(Renderer):
    """ DMXSerialRenderer provides a renderer interface to a custom DMX shield 
    using the RaspberryPi serial port. (TODO) It currently only supports a single
    universe.
    """ 

    __dmx_buffer_size = 512
    __default_channel_val = 0
    __device_name = "/dev/ttyAMA0"
    __baud_rateHz = 250000
    __timeout = 3.
    __bytesize = serial.EIGHTBITS
    __parity = serial.PARITY_NONE
    __stopbits = serial.STOPBITS_TWO
    
    def __init__(self, universes = 1):
        super(DMXSerialRenderer, self).__init__()        
        self.__port = serial.Serial(port = DMXSerialRenderer.__device_name)
        self.__port.baudrate = DMXSerialRenderer.__baud_rateHz
        self.__port.bytesize = DMXSerialRenderer.__bytesize
        self.__port.parity = DMXSerialRenderer.__parity
        self.__port.stopbits = DMXSerialRenderer.__stopbits
        self.__port.timeout = DMXSerialRenderer.__timeout
        # Initialize a shared storage buffer
        default_buffer = [DMXSerialRenderer.__default_channel_val]*DMXSerialRenderer.__dmx_buffer_size
        self.__buffer = {}
        for i in xrange(universes):
            self.__buffer[i] = bytearray(default_buffer)            
        
    def render(self, panel):
        # Fill in the buffer.
        for loc, pixel in panel.items():
            if pixel.live:
                universe = pixel.address.universe
                address = pixel.address.address
                self.__buffer[universe][address] = pixel.color.red
                self.__buffer[universe][address + 1] = pixel.color.green
                self.__buffer[universe][address + 2] = pixel.color.blue
        # Send the buffer over DMX.
        for universe, buf in self.__buffer.iteritems():
            self.__send_dmx(universe, buf)

    def __send_dmx(self, universe, buf):
        """ Sends the DMX packet over serial.
        """ 
        self.__port.baudrate = DMXSerialRenderer.__baud_rateHz/2
        self.__port.write(bytes([0]))
        self.__port.baudrate = DMXSerialRenderer.__baud_rateHz
        self.__port.write(bytes([0]))
        self.__port.write(buf)
        
    def __del__(self):
        self.__port.close()

    def __repr__(self):
        return "DMXSerialRenderer"        


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
        RPI.GPIO.setmode(RPI.GPIO.BOARD)
        RPI.GPIO.setwarnings(True)
        self.__pwm = []
        for channel in xrange(channels):
            RPI.GPIO.setup(channel, RPI.GPIO.OUT, initial = RPI.GPIO.LOW)
            self.__pwm.append(RPI.GPIO.PWM(channel, PiGPIORenderer.__pwm_frequencyHz))
            self.__pwm[channel].start(PiGPIORenderer.__pwm_init_dc)
        
    def render(self, panel):
        for loc, pixel in panel.items():
            assert pixel.address.universe is 0, "All pixels on universe 0."
            address = pixel.address.address
            norm = 255.
            self.__pwm[address].ChangeDutyCycle(pixel.color.red/norm)
            self.__pwm[address + 1].ChangeDutyCycle(pixel.color.green/norm)
            self.__pwm[address + 2].ChangeDutyCycle(pixel.color.blue/norm)

    def __del__(self):
        for pwm_channel in self.__pwm:
            pwm_channel.stop()
        RPI.GPIO.cleanup()

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
        RPI.GPIO.setmode(RPI.GPIO.BOARD)
        RPI.GPIO.setwarnings(True)
        assert len(channels) > 0, "Empty number of GPIO pins from RPi." 
        for channel in channels:
            RPI.GPIO.setup(channel, RPI.GPIO.OUT, initial = RPI.GPIO.LOW)            
        
    def render(self, panel):
        for loc, pixel in panel.items():
            assert pixel.address.universe is 0, "All pixels on universe 0."
            channel = pixel.address.address
            data = pixel.color.green << 16 | pixel.color.red << 8 | pixel.color.blue
            for i in xrange(PiToWS2812Renderer.__bit_width, -1, -1):
                if data & (1 << i):
                    RPI.GPIO.output(channel, RPI.GPIO.HIGH)
                    time.sleep(PiToWS2812Renderer.__sleep_T1HS)
                    RPI.GPIO.output(channel, RPI.GPIO.LOW)
                    time.sleep(PiToWS2812Renderer.__sleep_T1LS)
                else:
                    RPI.GPIO.output(channel, RPI.GPIO.HIGH)
                    time.sleep(PiToWS2812Renderer.__sleep_T0HS)
                    RPI.GPIO.output(channel, RPI.GPIO.LOW)
                    time.sleep(PiToWS2812Renderer.__sleep_T0LS)
            time.sleep(PiToWS2812Renderer.__sleep_resetS)

    def __del__(self):
        RPI.GPIO.cleanup()

    def __repr__(self):
        return "PiToWS2812Renderer"


class PyGameRenderer(Renderer):
    """ PyGameRenderer provides a renderer interface to a PyGame simulation client.
    Active (inactive) pixels are rendered as circles (squares).
    """

    __black = Color(0, 0, 0).rgba
    __font_color = Color(255, 255, 0).rgba
    __font_size = 10
    __default_font = "monospace"

    def __init__(self, 
                 size = (640, 480),
                 scale = 4, 
                 debug = False, 
                 universes = 1):
        super(PyGameRenderer, self).__init__(universes)
        pygame.init()
        self.__screen = pygame.display.set_mode(size)
        self.__screen.fill(PyGameRenderer.__black)
        self.__font = pygame.font.SysFont(PyGameRenderer.__default_font, 
                                          PyGameRenderer.__font_size)
        self.__scale = scale
        self.__debug = debug

    def render(self, panel):
        self.__screen.fill(PyGameRenderer.__black)
        width = self.__scale
        for loc, pixel in panel.items():
            if pixel.live:
                pygame.draw.circle(self.__screen, pixel.color.rgba, loc, width)
            else:
                x, y = loc
                rect = pygame.Rect(x - width, y + width, width, width)
                pygame.draw.rect(self.__screen, pixel.color.rgba, rect, width)
            # Print DMX address info in addition to color.
            if self.__debug:
                universe = pixel.address.universe
                address = pixel.address.address
                info = (universe, address)
                label = self.__font.render(str(info), 
                                           True,
                                           PyGameRenderer.__font_color)
                self.__screen.blit(label, loc)
        pygame.display.update()

    def __repr__(self):
        return "PyGameRenderer"
