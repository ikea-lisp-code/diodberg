 #! /usr/bin/env python

 # Include option for ignore cython distutils.

from distutils.core import setup
# from distutils.extension import Extension
# from Cython.Distutils import build_ext

setup(name='diodberg',
      version='0.1',
      description='Controller core and API for ikea-lisp-code climbing ball',
      author='Bhaskar Mookerji',
      author_email='mookerji@alum.mit.edu',
      url='http://spin-one.org',
      packages=['diodberg'],
      # cmdclass = {'build_ext': build_ext},
      # ext_modules = [Extension("dmxbuffer", ["ola_client/dmxbuffer.pyx"],
      #                          libraries=["ola", "olacommon", "protobuf"], language="c++"),
      #                Extension("olaclient", ["ola_client/olaclient.pyx"],
      #                          libraries=["ola", "olacommon", "protobuf"], language="c++"),
      #                Extension("olaclientwrapper", ["ola_client/olaclientwrapper.pyx"],
      #                          libraries=["ola", "olacommon", "protobuf"], language="c++"),
      #                Extension("streamingclient", ["ola_client/streamingclient.pyx"],
      #                          libraries=["ola", "olacommon", "protobuf"], language="c++")]
     )
