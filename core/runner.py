import time
import threading
try:
    import psyco
except ImportError:
    pass
else:
    psyco.full()


class Runner(threading.Thread):
    """ """

    __framecount = 0
    __default_sleep = 30
    
    def __init__(self, *args, **kwargs):
        threading.Thread.__init__(self, *args, **kwargs)
        self.__lock = thread.allocate_lock()
        self.daemon = True

    panel = property(__get_panel, __set_panel, __del_panel, "Panel.")
    name = property(__get_name, __set_name, __del_name, "Name.")
    renderer = property(__get_renderer, __set_renderer, __del_renderer, "Renderer.")

    def init(self, panel):
        """Initializes any environmental parameters based on the panel info.
        Defined by whatever subclasses Runner.""" 
        pass

    def fill(self):
        """Iterate over the panel and change the pixel RGB values.
        Defined by whatever subclasses runner."""
        pass

    def run(self):
        self.running = True
        self.__framecount = 0
        self.__last_tick = 0
        self.init(self.__panel)
        while self.running:
            if not self.__framecount % 30:
                tick = time.time()
                if self.__last_tick:
                    print "FPS: %0.2f" % (30 / (tick - self.__last_tick))
                self.__last_tick = tick
            self.__framecount += 1
            self.__lock.acquire()
            self.fill(self.__panel)
            self.__renderer.render(self.__panel)
            self.__lock.release()
            time.sleep(__default_sleep)
        
    def __get_panel(self): return self.panel
    def __set_panel(self, val): self.panel = val
    def __del_panel(self): del self.panel

    def __get_name(self): return self.name
    def __set_name(self, val): self.name = val
    def __del_name(self): del self.name

    def __get_renderer(self): return self.renderer
    def __set_renderer(self, val): self.renderer = val
    def __del_renderer(self): del self.renderer

    def __repr__(self):
        pass

#TODO: Extend to multiple threads
class Controller(object):
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
