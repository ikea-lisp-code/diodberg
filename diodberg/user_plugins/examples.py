# Example user-space applications for manipulating colors on panels.
# NOTE: If you're making a new application in this directory, I highly
# recommend adding a main() method so the script is 
# executable.


from diodberg.core.runner import Runner
from diodberg.util.utils import random_color


class ToggleColors(Runner):
    """ Random toggles colors. """

    def __init__(self, panel, renderer, sleep = 1):
        name = "ToggerColors"
        super(ToggleColors, self).__init__(panel, name, renderer, sleep)
    
    def init(self):
        pass

    def fill(self):
        for loc, pixel in self.panel.iteritems():
            r, g, b, alpha = random_color().rgba
            pixel.color.set_rgb(r, g, b)

    def __repr__(self):
        return super(ToggleColors, self).__repr__() + ":" + self.name


class CycleHue(Runner):
    """ Cycles hues. """

    def __init__(self, panel, renderer, sleep = 0.01):
        name = "CycleHue"
        super(CycleHue, self).__init__(panel, name, renderer)
    
    def init(self):
        pass

    def fill(self):
        for loc, pixel in self.panel.iteritems():
            h, s, v = pixel.color.hsv
            h = (h + 20) % 360
            pixel.color.set_hsv(h, s, v)

    def __repr__(self):
        return super(CycleHue, self).__repr__() + ":" + self.name


def simulation_main():
    """ Runs a simulation test routine for watching examples. """
    from diodberg.core.runner import Controller
    from diodberg.util.utils import random_panel
    from diodberg.renderers.simulation_renderers import PyGameRenderer
    panel = random_panel()
    renderer = PyGameRenderer(debug = True)
    runner = CycleHue(panel, renderer)
    controller = Controller(panel, renderer)
    controller.run(runner)

    
if __name__ == "main":
    simulation_main()
