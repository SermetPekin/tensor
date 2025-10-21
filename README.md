# Tensor Library

[![Test Build](https://github.com/SermetPekin/tensor/actions/workflows/test.yml/badge.svg)](https://github.com/SermetPekin/tensor/actions/workflows/test.yml)

A simple 1D tensor library with C extensions for high-performance computing, inspired by PyTorch.

In this module we build a small `Tensor` in C, along the lines of `torch.Tensor` or `numpy.ndarray`. The current code implements a simple 1-dimensional float tensor that we can access and slice. We get to see that the tensor object maintains both a `Storage` that holds the 1-dimensional data as it is in physical memory, and a `View` over that memory that has some start, end, and stride. This allows us to efficiently slice into a Tensor without creating any additional memory, because the `Storage` is re-used, while the `View` is updated to reflect the new start, end, and stride. We then get to see how we can wrap our C tensor into a Python module, just like PyTorch and numpy do.

## Building and Testing

The source code of the 1D Tensor is in [tensor/src/tensor1d.h](tensor/src/tensor1d.h) and [tensor/src/tensor1d.c](tensor/src/tensor1d.c). 

### Build C extension:

```bash
# Linux/macOS
cd tensor/src
gcc -O3 -shared -fPIC -o ../_tensor1d.so tensor1d.c -lm

# Windows  
cd tensor/src
gcc -O3 -shared -o ../_tensor1d.dll tensor1d.c
```

### Test:
```bash
python tensor/tests/test_simple.py
```

## Usage

```python
from tensor.tensor1d import Tensor

# Create tensors
t1 = Tensor.empty(5)        # [0.0, 0.0, 0.0, 0.0, 0.0]
t2 = Tensor.arange(5)       # [0.0, 1.0, 2.0, 3.0, 4.0]

# Indexing and slicing
print(t2[0])                # [0.0]
print(t2[1:4])              # [1.0, 2.0, 3.0]
print(t2[::2])              # [0.0, 2.0, 4.0]

# Arithmetic
t3 = t2.addf(5.0)           # [5.0, 6.0, 7.0, 8.0, 9.0]
t4 = t2.add(t2)             # [0.0, 2.0, 4.0, 6.0, 8.0]
```

### Standalone C program:

You can also compile and run the C code directly:

```bash
cd tensor/src
gcc -Wall -O3 tensor1d.c -o tensor1d -lm
./tensor1d
```

## Authors

- **Andrej Karpathy** - Original C implementation
- **SermetPekin** - Python packaging and cross-platform support

## License

MIT

The code contains both the `Tensor` class, and also a short `int main` that just has a toy example. We can now wrap up this C code into a Python module so we can access it there. For that, compile it as a shared library:

```bash
gcc -O3 -shared -fPIC -o libtensor1d.so tensor1d.c
```

This writes a `libtensor1d.so` shared library that we can load from Python using the [cffi](https://cffi.readthedocs.io/en/latest/) library, which you can see in the [tensor1d.py](tensor1d.py) file. We can then use this in Python simply like:

```python
import tensor1d

# 1D tensor of [0, 1, 2, ..., 19]
t = tensor1d.arange(20)

# getitem / setitem functionality
print(t[3]) # prints 3.0
t[-1] = 100.0 # sets the last element to 100.0

# slicing, prints [5, 7, 9, 11, 13]
print(t[5:15:2])

# slice of a slice works ok! prints [9, 11, 13]
# (note how the end range is oob and gets cropped)
print(t[5:15:2][2:7])

# add a scalar to the whole tensor
t = t + 10.0

# add two tensors (of the same size) together
t2 = tensor1d.arange(20)
t3 = t + t2

# add two tensors together with broadcasting
t4 = t + tensor1d.tensor([10.0])
```

Finally the tests use [pytest](https://docs.pytest.org/en/stable/) and can be found in [test_tensor1d.py](test_tensor1d.py). You can run this as `pytest test_tensor1d.py`.

It is well worth understanding this topic because you can get fairly fancy with torch tensors and you have to be careful and aware of the memory underlying your code, when we're creating new storage or just a new view, functions that may or may not only accept "contiguous" tensors. Another pitfall is when you e.g. create a small slice of a big tensor, assuming that somehow the big tensor will be garbage collected, but in reality the big tensor will still be around because the small slice is just a view over the big tensor's storage. The same would be true of our own tensor here.

Actual production-grade tensors like `torch.Tensor` have a lot more functionality we won't cover. You can have different `dtype` not just float, different `device`, different `layout`, and tensors can be quantized, encrypted, etc etc.

TODOs:

- bring our own implementation closer to `torch.Tensor`
- make tests better
- implement 2D tensor, where we have to start worrying about 2D shapes/strides
- implement broadcasting for 2D tensor

Good related resources:
- [PyTorch internals](http://blog.ezyang.com/2019/05/pytorch-internals/)
- [Numpy paper](https://arxiv.org/abs/1102.1523)

### License

MIT