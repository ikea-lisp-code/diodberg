import time
import threading

class Runner(threading.Thread):
    """ A Runner is the primary execution thread for a Panel visualization. An
    abstract class, it takes a Panel of pixels and a Renderer and executes 
    a rendering action for that panel.
    """ 
    
    __default_sleep = 30
    
    def __init__(self, panel, name, renderer):
        super(Runner, self).__init__()
        self.__lock = threading.Lock()
        self.daemon = True
        self.running = False
        self.__panel = panel
        self.__name = name
        self.__renderer = renderer
        self.__framecount = 0
        self.__last_tick = 0

    def init(self):
        """ Initializes any environmental parameters based on the panel info.
        Defined by whatever subclasses Runner.
        """ 
        pass

    def fill(self):
        """ Iterate over the panel and change the pixel RGB values.
        Defined by whatever subclasses runner.
        """
        pass

    def run(self):
        self.running = True        
        self.init()
        while self.running:
            if not self.__framecount % 30:
                tick = time.time()
                if self.__last_tick:
                    print "FPS: %0.2f" % (30 / (tick - self.__last_tick))
                self.__last_tick = tick
            self.__framecount += 1
            self.__lock.acquire()
            self.fill()
            self.__renderer.render(self.panel)
            self.__lock.release()
            time.sleep(Runner.__default_sleep)
        
    def __get_panel(self): 
        return self.__panel
    def __set_panel(self, val): 
        self.__panel = val
    def __del_panel(self): 
        del self.__panel

    def __get_name(self): 
        return self.__name
    def __set_name(self, val): 
        self.__name = val
    def __del_name(self): 
        del self.__name

    def __get_renderer(self): 
        return self.__renderer
    def __set_renderer(self, val): 
        self.__renderer = val
    def __del_renderer(self): 
        del self.__renderer

    panel = property(__get_panel, __set_panel, __del_panel, "Panel.")
    name = property(__get_name, __set_name, __del_name, "Name of visualization.")
    renderer = property(__get_renderer, __set_renderer, __del_renderer, "Renderer.")

    def __repr__(self):
        "Runner"

#TODO: Extend to multiple threads
class Controller(object):
    """ Controller initializes a set of Runner threads and shares execution between
    them. 
    """
    def __init__(self, panel, renderer):
        self.__panel = panel
        self.__renderer = renderer
        self.__running = False

    def run(self, runner):
        runner.panel = self.__panel
        runner.renderer = self.__renderer
        try:
            runner.start()
        except:
            runner.running = False
