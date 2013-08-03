# Random maybe useful utilities for panel manipulation.


class ConditionalDecorator(object):
    """ ConditionalDecorator allows conditional decoration at import time. It can
    be used to turn off numba's LLVM jit optimizations if you're you don't want
    them.
    """
    
    __slots__ = {'__condition', '__decorator'}

    def __init__(self, condition, decorator):
        self.__condition = condition
        self.__decorator = decorator

    def __call__(self, func):
        if not self.__condition:
            return func
        else:
            return self.__decorator(func)


def read_file(filename):
    """ Reads a file containing a specification of (possible multiple) panels. 
    TODO: Being changed to a JSON representation.
    """ 
    assert 0, "Not implemented yet."
    panels = dict()
    return panels
