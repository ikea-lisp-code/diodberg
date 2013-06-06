import pygame
from diodberg.core.renderer import Renderer
from diodberg.core.types import Color


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
                 scale = 6, 
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
        for loc, pixel in panel.iteritems():
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
