import pygame
import curses
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
    
    __slots__ = {'__screen', '__font', '__scale', '__debug'}

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


class CursesRenderer(Renderer):
    """ CursesRenderer is provides an in-terminal, curses-based renderer. 
    """ 

    __n_background = 0
    __ref_init = (0, 0)
    __win_size = (100, 100)
    __fg_scale = 1000./255.
    __slots__ = {'__stdscr', '__debug', '__has_color', '__win'}
    
    def __init__(self, debug = False):
        super(CursesRenderer, self).__init__()
        self.__debug = debug
        self.__stdscr = curses.initscr()
        self.__has_color = curses.has_colors() and curses.can_change_color()
        if self.__has_color:
            curses.start_color()
            curses.use_default_colors()
        size_x, size_y = CursesRenderer.__win_size
        init_x, init_y = CursesRenderer.__ref_init
        self.__win = curses.newwin(size_x, size_y, init_y, init_x)
        curses.noecho()
        curses.cbreak()
        curses.nl()
        self.__stdscr.keypad(True)        

    def render(self, panel):        
        self.__win.erase()
        self.__stdscr.clear()
        # fg_pair corresponds to pixel, which is foregrounded.
        fg_pair = 1
        for loc, pixel in panel.iteritems():
            x, y = loc
            if pixel.live or self.__debug:
                try:
                    if self.__has_color:
                        scale = CursesRenderer.__fg_scale
                        # curses colors range 0-1000
                        color = tuple(c/scale for p in pixel.color.rgba)                        
                        fg_color = curses.COLOR_WHITE + i
                        curses.init_color(fg_color, r, g, b)
                        curses.init_pair(fg_pair, fg_color, curses.COLOR_BLACK)
                        self.__win.addstr(y, x, 'X', curses.color_pair(fg_pair))
                    else: 
                        self.__win.addstr(y, x, 'X', curses.COLOR_WHITE)
                except curses.error:
                    print "curses error: TODO add proper logging!"
            if self.__debug:
                universe = pixel.address.universe
                address = pixel.address.address
                info = (universe, address)
                # TODO: Show the address here somewhere.
            fg_pair += 1
        self.__win.refresh()
    
    def __del__(self):
        curses.nocbreak()
        self.__stdscr.keypad(False) 
        curses.echo()
        curses.endwin()

    def __repr__(self):
        return "CursesRenderer"


def simulation_main():
    """ Runs a simulation test routine for watching examples. 
    """
    from diodberg.core.runner import Controller
    from diodberg.core.types import Panel
    from diodberg.user_plugins.examples import CycleHue
    from diodberg.renderers.simulation_renderers import PyGameRenderer
    panel = Panel.random_panel()
    renderer = PyGameRenderer(debug = True)
    runner = CycleHue(panel, renderer)
    controller = Controller(panel, renderer)
    controller.run(runner)


def test_curses():
    """ Tests the curses-based simulation.
    """ 
    import time
    from diodberg.core.types import Panel
    from diodberg.core.types import Color
    from diodberg.renderers.simulation_renderers import CursesRenderer
    panel = Panel.blank_panel()
    for loc, pixel in panel.iteritems():
        pixel.color = Color.random_color()
    renderer = CursesRenderer(debug = True)
    render.render(panel)
    time.sleep(100)
    

if __name__ == "__main__":
    test_curses()
