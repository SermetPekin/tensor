"""
Cross-platform CFFI build configuration for tensor package.
"""

import os
from cffi import FFI

def create_ffibuilder():
    """Create CFFI builder for cross-platform compilation."""
    
    ffibuilder = FFI()
    
    # Define the C interface
    ffibuilder.cdef("""
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
    """)
    
    # Platform-specific library linking
    libraries = []
    if os.name != 'nt':  # Unix-like systems (Linux, macOS)
        libraries = ["m"]  # Math library
    
    # Set the source
    ffibuilder.set_source(
        "tensor._tensor1d",
        """
        #include "tensor1d.h"
        """,
        sources=[os.path.join("tensor", "src", "tensor1d.c")],
        include_dirs=[os.path.join("tensor", "src")],
        libraries=libraries,
        extra_compile_args=["-O3", "-Wall"] if os.name != 'nt' else ["/O2"],
    )
    
    return ffibuilder

# This is used by setuptools when building
ffibuilder = create_ffibuilder()

if __name__ == "__main__":
    ffibuilder.compile(verbose=True)