# diodberg

diodberg is a new experimental climbing wall from 'ikea-lisp-code. 

Directory contents:
* core
  Basic types, runner, and rendering objects.
* docs
* firmware
  Device firmware for the climbing holds
* schematics
* user_plugins
  User applications for running visualizations
* util
  Misc.: Color manipulation and math utilities

# Package requirements
* Python 2.7 (?)
* Scipy/Numpy
## Optional (if you are working on protocol stuff):
* Cython
* Open Lighting Architecture (OLA)
* Google Protobufs
* cppunit

# Installation and setup instructions

  pkg-config --libs libola

  clang++ test.cpp -O4 -g -std=c++11 -stdlib=libc++ -L/usr/local/lib -lola -lolacommon -lprotobuf -o test

# Questions? 

Email <mookerji@spin-one.org>, <chris@notspelledright.com>
