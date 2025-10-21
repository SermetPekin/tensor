from setuptools import setup
from build_cffi import create_ffibuilder

# Create the CFFI builder
ffibuilder = create_ffibuilder()

setup(
    cffi_modules=["build_cffi.py:ffibuilder"],
)