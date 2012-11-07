'''
This is the setup script for BlitzCraft. To use this script to install the code
you should execute it with your python interpreter with the following command:

python setup.py install

Use "sudo" before that if you need administrative privileges on linux.

Visit http://docs.python.org/2/distutils/index.html for more info.
'''

from distutils.core import setup

#Check for dependencies before installing
dependencies = ['pymouse', 'gtk', 'numpy']
for dep in dependencies:
    try:
        __import__(dep)
    except ImportError:
        print('Missing dependency: {0} Please install this module'.format(dep))

setup(name='BlitzCraft',
      version='0.0.1',
      description='Educational tool for building bots to play Bejeweled Blitz',
      author='Paul Barton',
      author_email='pablo.barton@gmail.com',
      url='https://github.com/SavinaRoja/BlitzCraft',
      package_dir={'': 'src'},
      packages=['blitzcraft'],
      scripts=['scripts/'],
      #data_files=[('foo', ['foo/bar'])]
      )