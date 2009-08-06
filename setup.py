try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

setup(name='pygr-draw',
      version='0.5+20090805',
      description='pygr-draw draws pygr annotations',
      author = 'C. Titus Brown',
      author_email = 't@idyll.org',
      url = 'http://github.com/ctb/pygr-draw',
      license = 'BSD',
      packages = ['pygr_draw']
#      py_modules = ['client/pony_build_client'],
      )
