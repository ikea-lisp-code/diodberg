# Utilities for testing the serial protocol.

import sys
try:
    import serial
except ImportError as err:
    sys.stderr.write("Error: failed to import module ({})".format(err))


def write_dmx(baudrate = 115200, buf = bytearray([255, 255, 255])):
    """ Simple test routine for DMX-over-serial, with varying baudrates. The buf is
    the DMX address space (0 - 512). 
    TODO: The baudrate on the Pi currently ceilings at 115200 baud. Change back to 
    250000 baud when fixed on the Pi-side.
    """
    assert isinstance(buf, bytearray)
    num_addresses = 512
    assert len(buf) < num_addresses
    # DMX serial default parameters
    device_name = "/dev/ttyAMA0"
    port = serial.Serial(device_name)
    port.baudrate = baudrate
    port.bytesize = serial.EIGHTBITS
    port.parity = serial.PARITY_NONE
    port.stopbits = serial.STOPBITS_TWO
    port.timeout = 3.
    # Write break and mark-after-break
    port.baudrate = baudrate/2
    port.write(chr(0))
    # Write start and then values to address 0, 1, 2 
    # on universe 0
    port.baudrate = baudrate
    port.write(chr(0))
    port.write(buf)
    port.close()
