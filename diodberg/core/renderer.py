import array
import pygame
import sys
from diodberg.core.types import Color
try:
    from ola.ClientWrapper import ClientWrapper
except ImportError as err: 
    sys.stderr.write("Error: failed to import ola module ({})".format(err))


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
        for pixel in panel:
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


class PyGameRenderer(Renderer):
    """ PyGameRenderer provides a renderer interface to a PyGame simulation client.
    Active (inactive) pixels are rendered as circles (squares).
    """

    __default_x_size = 640
    __default_y_size = 480
    __default_size = (__default_x_size, __default_y_size)
    __default_scale = 4
    __black = Color(0, 0, 0).rgba
    __font_color = Color(255, 255, 0).rgba

    def __init__(self, 
                 size = (640, 480),
                 scale = 4, 
                 debug = False):
        super(PyGameRenderer, self).__init__()
        pygame.init()
        self.__screen = pygame.display.set_mode(size)
        self.__screen.fill(PyGameRenderer.__black)
        self.__font = pygame.font.SysFont("monospace", 10)
        self.__scale = scale
        self.__debug = debug

    def render(self, panel):
        self.__screen.fill(PyGameRenderer.__black)
        for loc, pixel in panel.items():
            if pixel.live:
                pygame.draw.circle(self.__screen, pixel.color.rgba, loc, self.__scale)
            else:
                x, y = loc
                rect = pygame.Rect(x - self.__scale, y + self.__scale, self.__scale, self.__scale)
                pygame.draw.rect(self.__screen, pixel.color.rgba, rect, self.__scale)
            # Print DMX address info in addition to color.
            if self.__debug:
                universe = pixel.address.universe
                address = pixel.address.address
                info = (universe, address)
                label = self.__font.render(str(info), 1, PyGameRenderer.__font_color)
                self.__screen.blit(label, loc)
        pygame.display.update()

    def __repr__(self):
        return "PyGameRenderer"
