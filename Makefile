# Cross-platform build settings
ifeq ($(OS),Windows_NT)
    CC = gcc
    SHARED_EXT = .dll
    SHARED_FLAGS = -shared
    LDFLAGS = 
else
    UNAME_S := $(shell uname -s)
    ifeq ($(UNAME_S),Linux)
        CC = gcc
        SHARED_EXT = .so
        SHARED_FLAGS = -shared -fPIC
        LDFLAGS = -lm
    endif
    ifeq ($(UNAME_S),Darwin)
        CC = gcc
        SHARED_EXT = .so
        SHARED_FLAGS = -shared -fPIC
        LDFLAGS = -lm
    endif
endif

CFLAGS = -Wall -O3
PYTHON = python3

# turn on all the warnings
# https://github.com/mcinglis/c-style
CFLAGS += -Wall -Wextra -Wpedantic \
          -Wformat=2 -Wno-unused-parameter -Wshadow \
          -Wwrite-strings -Wstrict-prototypes -Wold-style-definition \
          -Wredundant-decls -Wnested-externs -Wmissing-include-dirs

# Source files
SRC_DIR = tensor/src
C_FILES = $(SRC_DIR)/tensor1d.c
H_FILES = $(SRC_DIR)/tensor1d.h

# Main targets
all: tensor1d libtensor1d.so

# Compile the main executable
tensor1d: $(C_FILES) $(H_FILES)
	cd $(SRC_DIR) && $(CC) $(CFLAGS) -o ../../$@ tensor1d.c $(LDFLAGS)

# Create shared library
libtensor1d$(SHARED_EXT): $(C_FILES) $(H_FILES)
	cd $(SRC_DIR) && $(CC) $(CFLAGS) $(SHARED_FLAGS) -o ../../libtensor1d$(SHARED_EXT) tensor1d.c $(LDFLAGS)

# Build CFFI extension
cffi: $(C_FILES) $(H_FILES)
	cd $(SRC_DIR) && $(PYTHON) build_cffi.py

# Build Python package
build: cffi
	$(PYTHON) -m build

# Install package in development mode
install-dev:
	$(PYTHON) -m pip install -e .[dev]

# Install package
install:
	$(PYTHON) -m pip install .

# Test using pytest
test:
	$(PYTHON) -m pytest tensor/tests/ -v

# Run tests with coverage
test-cov:
	$(PYTHON) -m pytest tensor/tests/ --cov=tensor --cov-report=html --cov-report=term

# Format code
format:
	$(PYTHON) -m black tensor/
	$(PYTHON) -m isort tensor/

# Type checking
typecheck:
	$(PYTHON) -m mypy tensor/

# Lint code
lint: format typecheck

# Clean up build artifacts
clean:
	rm -f tensor1d libtensor1d.so
	rm -rf build/ dist/ *.egg-info/
	rm -rf tensor/__pycache__/ tensor/tests/__pycache__/
	rm -rf .pytest_cache/ .coverage htmlcov/
	find . -name "*.pyc" -delete
	find . -name "*.so" -delete
	find . -name "_tensor1d*" -delete

# Clean everything including virtual environments
clean-all: clean
	rm -rf .venv/ venv/

# Help
help:
	@echo "Available targets:"
	@echo "  all          - Build C executable and shared library"
	@echo "  tensor1d     - Build C executable"
	@echo "  libtensor1d.so - Build shared library"
	@echo "  cffi         - Build CFFI extension"
	@echo "  build        - Build Python package"
	@echo "  install-dev  - Install package in development mode"
	@echo "  install      - Install package"
	@echo "  test         - Run tests"
	@echo "  test-cov     - Run tests with coverage"
	@echo "  format       - Format code with black and isort"
	@echo "  typecheck    - Run mypy type checking"
	@echo "  lint         - Run formatting and type checking"
	@echo "  clean        - Clean build artifacts"
	@echo "  clean-all    - Clean everything including virtual environments"
	@echo "  help         - Show this help message"

.PHONY: all clean clean-all test test-cov tensor1d cffi build install-dev install format typecheck lint help
