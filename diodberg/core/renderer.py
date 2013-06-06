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
