"""A setuptools based setup module.
See:
https://packaging.python.org/en/latest/distributing.html
https://github.com/pypa/sampleproject
"""

# Always prefer setuptools over distutils
from setuptools import setup, find_packages
# To use a consistent encoding
#from codecs import open
from os import path

setup(
    name='sample',

    version='1.2.0',

    description='DonkeyKong game',
    author='R V Sahithi',
    author_email='sahithi.rv@students.iiit.ac.in',
    license='MIT',

    install_requires=['pygame']
)
