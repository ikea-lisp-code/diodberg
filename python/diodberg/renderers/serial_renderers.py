from diodberg.core.renderer import Renderer
import sys
try:
    import serial
except ImportError as err: 
    sys.stderr.write("Error: failed to import module ({})".format(err))


class DMXSerialRenderer(Renderer):
    """ DMXSerialRenderer provides a renderer interface to a custom DMX shield 
    using the RaspberryPi serial port.
    TODO: The baudrate on the Pi currently ceilings at 115200 baud. Change back to 
    250000 baud when fixed on the Pi-side.
    """ 

    __dmx_buffer_size = 512
    __default_channel_val = 0
    __device_name = "/dev/ttyAMA0"
    __baud_rateHz = 115200
    __timeout = 3.
    __bytesize = serial.EIGHTBITS
    __parity = serial.PARITY_NONE
    __stopbits = serial.STOPBITS_TWO

    __slots__ = {'__port', '__buffer'}
    
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
        for loc, pixel in panel.iteritems():
            if pixel.live:
                universe = pixel.address.universe
                address = pixel.address.address
                self.__buffer[universe][address] = pixel.color.red
                self.__buffer[universe][address + 1] = pixel.color.green
                self.__buffer[universe][address + 2] = pixel.color.blue
        # Send the buffer over DMX.
        for universe, buf in self.__buffer.iteritems():
            self.send_dmx(universe, buf)

    def send_dmx(self, universe, buf):
        """ Sends the DMX packet over serial.
        """ 
        self.__port.baudrate = DMXSerialRenderer.__baud_rateHz/2
        self.__port.write(chr(0))
        self.__port.baudrate = DMXSerialRenderer.__baud_rateHz
        self.__port.write(chr(0))
        self.__port.write(buf)

    def close(self):
        """ Close the serial port.
        """
        self.__port.close()
        
    def __del__(self):
        self.close()

    def __repr__(self):
        return "DMXSerialRenderer"


def pi_serial_main(num = 1):
    """ Runs a test routine for testing serial DMX output."""
    from diodberg.core.runner import Controller
    from diodberg.core.types import random_panel
    from diodberg.user_plugins.examples import CycleHue
    panel = random_panel(size = (num, 1), num_pixels = num, live = True)
    renderer = DMXSerialRenderer()
    runner = CycleHue(panel, renderer, sleep = 1.)
    controller = Controller(panel, renderer)
    controller.run(runner)
    

if __name__ == "__main__":
    pi_serial_main()
