from distutils.core import setup, Extension

example_module = Extension('_bmath', sources=['bmath.c', 'bmath.i'])
setup(name='bmath', ext_modules=[example_module], py_modules=["bmath"])