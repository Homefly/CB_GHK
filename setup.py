from setuptools import setup, find_packages  # Always prefer setuptools over distutils
from codecs import open  # To use a consistent encoding
from os import path
import CBFilter

# Get the long description from the relevant file
with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()


setup(
    packages = find_packages(where="src"),
    package_dir = {"": "src"},
    setup_requires = ['pytest-runner'],
    tests_require = ['pytest'],
)