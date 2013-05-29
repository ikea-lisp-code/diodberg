import array
import pygame
from pygame.locals import *
from types import Color
from ola.ClientWrapper import ClientWrapper


class Renderer(object):
    """Renderer is an abstract base class for objects that actually render pixels
    that have been filled in.
    """ 

    def __init__(self, universes = 1):
        pass
    
    def render(self, panel):
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
        # Initialize a shared storage buffer
        default_buffer = [__default_channel_val]*__dmx_buffer_size
        self.__buffer = {}
        for i in xrange(universes):
            self.__buffer[i] = array.array('B', default_buffer)
        self.__wrapper = ClientWrapper()
        self.__client = wrapper.Client()

    def render(self, panel):
        # Fill in the buffer.
        for pixel in panel:
            if pixel.live:
                universe = pixel.address.universe
                address = pixel.address.address
                self.__buffer[universe][address] = pixel.color.red
                self.__buffer[universe][address + 1] = pixel.color.green
                self.__buffer[universe][address + 2] = pixel.color.blue
        for universe, buf in self.__buffer.iteritems():
            self.__client.SendDmx(universe, buf, __dmx_sent)
            self.__wrapper.Run()
        
    def __dmx_sent(state):
        self.__wrapper.Stop()

    def __repr__(self):
        return "DMXRenderer"


class PyGameRenderer(object):
    """PyGameRenderer provides a renderer interface to a PyGame simulation client.
    """

    __default_x_size = 640
    __default_y_size = 480
    __default_size = (__default_x_size, __default_y_size)
    __default_scale = 1
    __black = Color(0, 0, 0).raw
    __font = pygame.font.SysFont("monospace", 10)
    __font_color = Color(255, 255, 0).raw

    def __init__(self, 
                 size = (__default_x_size, __default_y_size), 
                 scale = __default_scale, 
                 debug = False):
        pygame.init()
        self.__screen = pygame.display.set_mode(__default_size)
        self.__screen.fill(__black)
        self.__scale = scale
        self.__debug = debug

    def render(self, panel):
        self.__screen.fill(__black)
        for loc, pixel in panel:            
            color = pixel.color.raw
            if pixel.live:
                pygame.draw.circle(self.__screen, color, loc, self.__scale)
            else:
                pygame.draw.rect(self.__screen, color, loc, self.__scale)
            if self.__debug:
                universe = pixel.address.universe
                address = pixel.address.address
                info = (universe, address)
                label = font.render(str(info), __font_color)
                self.__screen.blit(label, loc)
        pygame.display.update()

    def __repr__(self):
        return "PyGameRenderer"
