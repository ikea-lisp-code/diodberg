 #! /usr/bin/env python

from distutils.core import setup

# I do not really recommend installing this on your system.

setup(name = 'diodberg',
      version = '0.0.1',
      description = 'Controller core and API for ikea-lisp-code climbing ball',
      author = 'Bhaskar Mookerji',
      author_email = 'mookerji@alum.mit.edu',
      url = 'http://spin-one.org',
      packages = ['diodberg', 
                  'diodberg.core.types', 
                  'diodberg.core.runner',
                  'diodberg.core.renderer',
                  'diodberg.renderers.serial_renderers', 
                  'diodberg.renderers.simulation_renderers',
                  'diodberg.renderers.gpio_renderers',
                  'diodberg.user_plugins.examples',
                  'diodberg.util.utils',
                  'diodberg.util.serial_utils'],
      classifiers = ["Development Status :: 2 - Pre-Alpha",
                     "Environment :: Console"]
  )
