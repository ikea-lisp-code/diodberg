# Core types and Python boilerplate for defining pixels, panels, thread-safe
# core objects, etc. I would have used collections, but I've prefer to have
# some data safety.

from collections import MutableMapping
import sys
try: 
    from scipy.spatial import cKDTree
except ImportError as err: 
    sys.stderr.write("Error: failed to import scipy.spatial module ({})".format(err))


class Color(object):
    """ RGB color representation. Saturates for invalid values.
    """

    __min = 0
    __max = 255
    __size = 4

    def __init__(self, red = 0, green = 0, blue = 0, alpha = 0):
        self.__color = bytearray([0, 0, 0, 0])
        self.red = red
        self.green = green
        self.blue = blue
        self.alpha = alpha

    @property
    def raw(self):
        return (self.red, self.green, self.blue, self.alpha)

    def set_rgb(self, red, green, blue, alpha = 0):
        self.red = red
        self.green = green
        self.blue = blue
        self.alpha = alpha

    # Red channel
    def __get_r(self): 
        return self.__color[0]
    def __set_r(self, val): 
        self.__set_val(0, val)

    # Green channel
    def __get_g(self): 
        return self.__color[1]
    def __set_g(self, val): 
        self.__set_val(1, val)

    # Blue channel
    def __get_b(self): 
        return self.__color[2]
    def __set_b(self, val): 
        self.__set_val(2, val)

    # Alpha channel
    def __get_a(self): 
        return self.__color[3]
    def __set_a(self, val): 
        self.__set_val(3, val)

    def __set_val(self, index, val):
        assert index < Color.__size
        try:
            self.__color[index] = val
        except ValueError:
            if val > Color.__max:
                self.__color[index] = Color.__max
            else: 
                self.__color[index] = Color.__min

    red = property(__get_r, __set_r, None, "Red channel.")    
    green = property(__get_g, __set_g, None, "Green channel.")
    blue = property(__get_b, __set_b, None, "Blue channel.")
    alpha = property(__get_a, __set_a, None, "Alpha channel.")

    def __repr__(self):
        val = (self.red, self.green, self.blue, self.alpha)
        formatted = "<Color (r = %0.3f, g = %0.3f, b = %0.3f, alpha = %0.3f)>"
        return formatted % val


class Location(object):
    def __init__(self, x = 0, y = 0):
        self.__x = x
        self.__y = y
    
    @property
    def raw(self):
        return (self.x, self.y)

    def set_loc(self, x, y):
        self.x = x
        self.y = y

    def __get_x(self): 
        return self.__x
    def __set_x(self, val): 
        self.__x = val
    def __del_x(self): 
        del self.__x

    def __get_y(self): 
        return self.__y
    def __set_y(self, val): 
        self.__y = val
    def __del_y(self): 
        del self.__y

    x = property(__get_x, __set_x, __del_x, "Horizontal x.")
    y = property(__get_y, __set_y, __del_y, "Vertical y.")
    
    def __repr__(self):
        formatted = "<Location (x = %0.3f, y = %0.3f)>"
        return formatted % (self.x, self.y)


class DMXAddress(object):
    """Defines the DMX address for a live pixel.
    """
    __invalid_address = -1
    __dmx_lower = 0
    __dmx_upper = 512
    
    def __init__(self, universe = 0, address = 0):
        self.__universe = universe
        self.__address = 0
        self.address = address

    def is_valid(self): 
        return self.address is not DMXAddress.__invalid_address

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
    
    def __init__(self, 
                 color = Color(), 
                 location = Location(), 
                 address = DMXAddress(), 
                 live = False):
        self.__color = color
        self.__location = location
        self.__address = address
        self.__live = live
        assert not live or (live and address.is_valid())            
        
    def __get_color(self): 
        return self.__color
    def __set_color(self, val): 
        self.__color = val
    def __del_color(self): 
        del self.__color    

    def __get_location(self): 
        return self.__location
    def __set_location(self, val): 
        self.__location = val
    def __del_location(self): 
        del self.__location

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
    location = property(__get_location, __set_location, __del_location, "Location (x, y).")
    address = property(__get_address, __set_address, __del_address, "DMX address.")
    live = property(__get_live, __set_live, __del_live, "Is live pixel?")

    def __repr__(self):
        return "".join(["<Pixel ", 
                        str(self.color), ",", 
                        str(self.location), ", live = ", 
                        str(self.live), ">"])


class Panel(MutableMapping):
    """ Panel represents a collection of pixels, representing a climbing wall.
    It's structured as a dictionary with fast k-nearest neighbor access of 
    pixels.
    """ 
    
    def __init__(self):
        self.__pixels = dict()
        if len(self.locations) > 0:
            self.__tree = cKDTree(self.locations)
        else: 
            self.__tree = None

    @property
    def locations(self):
        """ Returns an array of (x, y) tuple locations for pixels.
        """
        return self.__pixels.keys()

    def get_nearest(self, location, num_pixels):
        """ Returns the num_pixels closests pixels to a location. 
        """
        assert self.__tree, "__tree is empty."
        return self.__tree.query_ball_point(location, num_pixels)

    def __contains__(self, key):
        return key in self.__pixels

    def __getitem__(self, key):
        return self.__pixels[key]

    def __setitem__(self, key, value):
        if key not in self.__pixels:
            self.__tree = cKDTree(self.locations + [key])
        self.__pixels[key] = value

    def __delitem__(self, key):
        del self.__pixels[key]

    def __len__(self):
        return len(self.__pixels)

    def __iter__(self):
        return iter(self.__pixels)
    
    def __repr__(self):
        return self.__pixels.__repr__()
