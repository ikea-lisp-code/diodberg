# Core types and Python boilerplate for defining pixels, panels, thread-safe
# core objects, etc. I would have used collections, but I've prefer to have
# some data safety.

from collections import MutableMapping
import colorsys
import random


class Color(object):
    """ Color representation, stored as RGB. Saturates for invalid values (FIX).
    """

    __min = 0           # RGB min
    __max = 255         # RGB max
    __hue_max = 360.    # Hue max
    
    __slots__ = {'red', 'green', 'blue', 'alpha'}

    def __init__(self, red = 0, green = 0, blue = 0, alpha = 0):
        self.red = red
        self.green = green
        self.blue = blue
        self.alpha = alpha
        
    @classmethod
    def random_color(cls):
        """ Returns a random Color.
        """
        r, g, b = [random.randint(0, 255) for i in range(3)]
        return Color(r, g, b)

    @property
    def rgba(self):
        """ Raw RGB-Alpha tuple (not normalized).
        """
        return (self.red, self.green, self.blue, self.alpha)

    @property
    def hsv(self):
        """ HSV tuple (not normalized).
        """
        norm = float(Color.__max)
        h, s, v = colorsys.rgb_to_hsv(self.red/norm, self.green/norm, self.blue/norm)
        return (Color.__hue_max*h, s, v)

    def set_rgb(self, red, green, blue, alpha = 0):
        """ Set RGB convenience method.
        """ 
        self.red = red
        self.green = green
        self.blue = blue
        self.alpha = alpha

    def set_hsv(self, hue, saturation, value):
        """ Set HSV convenience method. Assumes that a max range of (360., 1., 1.).
        """ 
        norm_hue = hue/Color.__hue_max
        red, green, blue = colorsys.hsv_to_rgb(norm_hue, saturation, value)
        self.red = int(round(red*Color.__max))
        self.green = int(round(green*Color.__max))
        self.blue = int(round(blue*Color.__max))

    def __repr__(self):
        val = (self.red, self.green, self.blue, self.alpha)
        formatted = "<Color (r = %0.3f, g = %0.3f, b = %0.3f, alpha = %0.3f)>"
        return formatted % val


class DMXAddress(object):
    """Defines the DMX address for a live pixel.
    """
    __invalid_address = -1
    __dmx_lower = 0
    __dmx_upper = 512

    __slots__ = {'__universe', '__address'}
    
    def __init__(self, universe = 0, address = 0):
        self.__universe = universe
        self.__address = address

    def is_valid(self): 
        return self.__address is not DMXAddress.__invalid_address

    def __get_universe(self): 
        return self.__universe
    def __set_universe(self, val): 
        self.__universe = val
    def __del_universe(self): 
        del self.__universe

    def __get_address(self): 
        return self.__address
    def __set_address(self, val):
        if DMXAddress.__dmx_lower <= val <= DMXAddress.__dmx_upper:
            self.__address = val
        else:
            self.__address = DMXAddress.__invalid_address
    def __del_address(self): 
        del self.__address

    universe = property(__get_universe, __set_universe, __del_universe, "DMX universe.")
    address = property(__get_address, __set_address, __del_address, "DMX address.")

    def __repr__(self):
        formatted = "<DMXAddress (universe = %0.3f, address = %0.3f)>"
        return formatted % (self.universe, self.address)
    

class Pixel(object):
    """ A pixel has a color and location. If it is live, it must have a valid
    DMX address.
    """
    
    __slots__ = {'__color', '__address', '__live'}
    
    def __init__(self, 
                 color = Color(), 
                 address = DMXAddress(), 
                 live = False):
        self.__color = color
        self.__address = address
        self.__live = live
        assert not live or (live and address.is_valid())            
        
    def __get_color(self): 
        return self.__color
    def __set_color(self, val): 
        self.__color = val
    def __del_color(self): 
        del self.__color    

    def __get_address(self): 
        return self.__address
    def __set_address(self, val): 
        self.__address = val
    def __del_address(self): 
        del self.__address

    def __get_live(self): 
        return self.__live
    def __set_live(self, val): 
        self.__live = val
    def __del_live(self): 
        del self.__live

    color = property(__get_color, __set_color, __del_color, "RGB color.")
    address = property(__get_address, __set_address, __del_address, "DMX address.")
    live = property(__get_live, __set_live, __del_live, "Is live pixel?")

    def __repr__(self):
        return "".join(["<Pixel ", 
                        str(self.color), ",", 
                        "live = ", str(self.live), ">"])


class Panel(MutableMapping):
    """ Panel represents a collection of pixels, representing a climbing wall.
    It's structured as a dictionary with fast k-nearest neighbor access of
    pixels.
    """

    __slots__ = {'__pixels'}

    def __init__(self):
        self.__pixels = dict()

    @property
    def locations(self):
        """ Returns an array of (x, y) tuple locations for pixels.
        """
        return self.__pixels.keys()

    @property
    def addresses(self):
        """ Returns a dictionary, keyed by DMX universe, of available DMX
        addresses.
        """
        address_dict = dict()
        for loc, pixel in self.__pixels.items():
            address = pixel.address.address
            universe = pixel.address.universe
            if universe not in address_dict:
                address_dict[universe] = [address]
            else:
                address_dict[universe].append(address)
        return address_dict

    def __contains__(self, key):
        return key in self.__pixels

    def __getitem__(self, key):
        return self.__pixels[key]

    def __setitem__(self, key, value):
        self.__pixels[key] = value

    def __delitem__(self, key):
        del self.__pixels[key]

    def __len__(self):
        return len(self.__pixels)

    def __iter__(self):
        return iter(self.__pixels)

    def __repr__(self):
        return self.__pixels.__repr__()
