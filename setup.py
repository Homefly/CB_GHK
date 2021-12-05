from setuptools import setup
from setuptools import find_packages

setup(
    packages = find_packages(where="src"),
    package_dir = {"": "src"},
    setup_requires = ['pytest-runner'],
    tests_require = ['pytest'],
)