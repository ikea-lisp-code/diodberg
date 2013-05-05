# Core types and Python boilerplate for defining pixels, panels, thread-safe
# core objects, etc. I would have used collections, but I've prefer to have
# some data safety.

# TODO: Debug

import pdb
import threading
import thread
from scipy.spatial import cKDTree
from collections import MutableMapping        

class Color(object):
    """ RGB color representation. Saturates for invalid values."""
    __rgb_lower = 0
    __rgb_upper = 255
    def __init__(self, r = 0, g = 0, b = 0, alpha = 0):
        self.red = r
        self.green = g
        self.blue = b
        self.alpha = alpha

    red = property(__get_r, __set_r, __del_r, "Red channel")    
    green = property(__get_g, __set_g, __del_g, "Green channel")
    blue = property(__get_b, __set_b, __del_b, "Blue channel")
    alpha = property(__get_a, __set_a, __del_a, "Alpha channel")

    def set_rgb(self, red, green, blue, alpha = 0):
        self.red = red
        self.red = green
        self.blue = blue
        self.alpha = alpha
    
    def __get_r(self): return self.red
    def __set_r(self, val):
        if __rgb_lower <= val <= __rgb_upper:
            self.red = val
        else
            self.red = __rgb_upper if val > __rgb_upper else __rgb_lower
    def __del_r(self): del self.red    

    def __get_g(self): return self.green
    def __set_g(self, val):
        if __rgb_lower <= val <= __rgb_upper:
            self.green = val
        else
            self.green = __rgb_upper if val > __rgb_upper else __rgb_lower
    def __del_g(self): del self.green

    def __get_b(self): return self.blue
    def __set_b(self, val):
        if __rgb_lower <= val <= __rgb_upper:
            self.blue = val
        else
            self.blue = __rgb_upper if val > __rgb_upper else __rgb_lower            
    def __del_b(self): del self.blue

    def __get_a(self): return self.alpha
    def __set_a(self, val):
        if __rgb_lower <= val <= __rgb_upper:
            self.alpha = val
        else
            self.alpha = __rgb_upper if val > __rgb_upper else __rgb_lower            
    def __del_a(self): del self.alpha

    def __repr__(self):
        val = (red, green, blue, alpha)
        formatted = "<Color (r = %0.3f, g = %0.3f, b = %0.3f, alpha = $%0.3f)>"
        return formatted % val    


dmx# TODO: (optional) Range checking?
class Location(object):
    def __init__(self, x = 0, y = 0):
        self.x = x
        self.y = y

    x = property(__get_x, __set_x, __del_x, "Horizontal x.")
    y = property(__get_y, __set_y, __del_y, "Vertical y.")

    @property
    def location(self):
        return (self.x, self.y)

    def set_loc(self, x, y):
        self.x = x
        self.y = y    

    def __get_x(self): return self.x
    def __set_x(self, val): self.x = val
    def __del_x(self): del self.x

    def __get_y(self): return self.x
    def __set_y(self, val): self.x = val
    def __del_y(self): del self.x
    
    def __repr__(self):
        formatted = "<Location (x = %0.3f, y = %0.3f)>"
        return formatted % (x, y)


class DMXAddress(object):
    """Defines the DMX address for a live pixel."""
    __invalid_address = -1
    __dmx_lower = 0
    __dmx_upper = 512
    
    def __init__(self, universe = 0, address = 0):
        self.universe = universe
        self.address = address

    universe = property(__get_universe, __set_universe, __del_universe, "DMX universe.")
    address = property(__get_address, __set_address, __del_address, "DMX address.")

    def has_valid_address(): return self.address is not __invalid_address

    def __get_universe(self): return self.universe
    def __set_universe(self, val): self.universe = val
    def __del_universe(self): del self.universe

    def __get_address(self): return self.address
    def __set_address(self, val):
        self.address = val if __dmx_lower <= val < = __dmx_upper else __invalid_address
    def __del_address(self): del self.address    

    def __repr__(self):
        formatted = "<DMXAddress (universe = %0.3f, address = %0.3f)>"
        return formatted % (universe, address)
    

class Pixel(object):
    """A pixel has a color and location. If it is live, it must have a valid
    DMX address."""
    
    def __init__(self, color = Color(), location = Location(), address = DMXAddress(), live = False):
        self.color = color
        self.location = location
        self.address = address
        self.live = live
        assert not live or (live and address.has_valid_address())        

    color = property(__get_color, __set_color, __del_color, "RGB color.")
    location = property(__get_location, __set_location, __del_location, "Location (x, y).")
    address = property(__get_address, __set_address, __del_address, "DMX address.")
    live = property(__get_live, __set_live, __del_live, "Is live pixel?")
        
    def __get_color(self): return self.color
    def __set_color(self, val): self.color = val
    def __del_color(self): del self.color    

    def __get_location(self): return self.location
    def __set_location(self, val): self.location = val
    def __del_location(self): del self.location

    def __get_address(self): return self.address
    def __set_address(self, val): self.address = val
    def __del_address(self): del self.address

    def __get_live(self): return self.live
    def __set_live(self, val): self.live = val
    def __del_live(self): del self.live

    def __repr__(self):
        return "".join(["<Pixel ", color, ",", location, ", live = ", live, ">"])


class Panel(MutableMapping):
    def __init__(self, pixels):
        self.__pixels = dict(pixels)
        self.__tree = cKDTree(self.locations)

    @property
    def locations(self):
        """ Returns an array of (x, y) tuple locations for pixels."""
        return self.__pixels.keys()

    def get_nearest(self, location, num_pixels):
        """ Returns the num_pixels closests pixels to a location. """
        return self.__tree.query_ball_point(location, num_pixels)

    def __contains__(self, key):
        return key in self.__pixels

    def __getitem__(self, key):
        return self.__pixels[key]

    def __setitem__(self, key, value):
        if key not in self.__pixels:
            self.__tree = cKDTree(self.locations.append(key))
        self.__pixels[key] = value

    def __delitem__(self, key):
        del self.__pixels[key]

    def __len__(self):
        return len(self.__pixels)

    def __iter__(self):
        return iter(self.__pixels)
    
    def __repr__(self):
        return self.__pixels.__repr__()
