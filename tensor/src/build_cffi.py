#!/usr/bin/env python3
"""
Build script for CFFI extension.
This script compiles the C extension for the tensor library.
"""

import os
import sys
from cffi import FFI

def build_extension():
    """Build the CFFI extension."""
    
    # Get the directory containing this script
    here = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(here)
    
    # Setup CFFI
    ffibuilder = FFI()
    
    # Define the C interface
    cdef_content = """
    typedef struct {
        float* data;
        int data_size;
        int ref_count;
    } Storage;

    typedef struct {
        Storage* storage;
        int offset;
        int size;
        int stride;
        char* repr;
    } Tensor;

    Tensor* tensor_empty(int size);
    int logical_to_physical(Tensor *t, int ix);
    float tensor_getitem(Tensor* t, int ix);
    Tensor* tensor_getitem_astensor(Tensor* t, int ix);
    float tensor_item(Tensor* t);
    void tensor_setitem(Tensor* t, int ix, float val);
    Tensor* tensor_arange(int size);
    char* tensor_to_string(Tensor* t);
    void tensor_print(Tensor* t);
    Tensor* tensor_slice(Tensor* t, int start, int end, int step);
    Tensor* tensor_addf(Tensor* t, float val);
    Tensor* tensor_add(Tensor* t1, Tensor* t2);
    void tensor_incref(Tensor* t);
    void tensor_decref(Tensor* t);
    void tensor_free(Tensor* t);
    """
    
    ffibuilder.cdef(cdef_content)
    
    # Set the source
    ffibuilder.set_source(
        "_tensor1d",  # Module name
        """
        #include "tensor1d.h"
        """,
        sources=["tensor1d.c"],
        include_dirs=["."],
        libraries=["m"],  # Link with math library
        extra_compile_args=["-O3", "-Wall", "-Wextra"],
    )
    
    # Compile the extension
    print("Building CFFI extension...")
    ffibuilder.compile(verbose=True)
    print("Extension built successfully!")

if __name__ == "__main__":
    build_extension()