# diodberg

diodberg runs new experimental climbing wall from 'ikea-lisp-code. 

If you are currently working on the wall, I recommend just checking out the
repository directly and using classes through the directory hierarchy instead
of using the setup.py file.

Directory/package contents:
* diodberg/core

  Basic types, runner, and rendering objects. User applications interact with
  the wall by directly manipulating pixels on a Panel through an iterator
  interface. This is a strong candidate for future performance improvements.

* diodberg/input
  
  Nothing here! Currently, we lack both software and hardware support for
  sensor input to the wall while in-flight.

* diodberg/user_plugins

  User applications for running visualizations. If you are writing an
  application to run on the wall, check out things here.

* diodberg/renderers

  Simulation, serial, and GPIO interfaces for driving lights.

* diodberg/util

  Misc.: random utilities

...and: 
* docs
* firmware

  Device firmware for DMX intermediaries

* schematics


# Package requirements
* Python 2.7 
* Pygame (for simulating plugins)
* If working on protocol stuff: pyserial and RPi
* Eventually: numpy/scipy


# Installation and setup instructions
  
  TODO (see above)

# Questions? 

Email <mookerji@spin-one.org>, <chris@notspelledright.com>, <yuanyu.chen@gmail.com>
