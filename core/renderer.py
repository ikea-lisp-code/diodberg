import array
from ola.ClientWrapper import ClientWrapper

class Renderer(threading.Thread):
    def __init__(self, panel):
        pass
    
    def render(self, panel):
        pass

    def __repr__(self):
        pass

class DMXRenderer(Renderer):
    """ DMXRenderer provides a renderer interface to the OLA client. You should
    specify the number of DMX universes panel pixels are spread over."""
    
    __dmx_buffer_size = 512
    __default_channel_val = 0
    
    def __init__(self, universes = 1):
        self.__wrapper = ClientWrapper()
        self.__client = wrapper.Client()
        default_buffer = [__default_channel_val]*__dmx_buffer_size
        self.__buffer = {}
        for i in xrange(universes):
            self.__buffer[i] = array.array('B', default_buffer)

    def render(self, panel):
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
