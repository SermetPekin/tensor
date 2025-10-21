"""
Basic tests for tensor1d functionality without external dependencies.
"""
import pytest
import sys
import os

# Add the project root to the path so we can import tensor
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from tensor.tensor1d import Tensor


class TestTensorBasic:
    """Basic functionality tests that don't require external libraries."""

    def test_import(self):
        """Test that we can import the tensor module."""
        from tensor.tensor1d import Tensor
        assert Tensor is not None

    def test_empty_tensor_creation(self):
        """Test creating empty tensors of different sizes."""
        # Test different sizes
        for size in [0, 1, 5, 10]:
            t = Tensor.empty(size)
            assert len(t) == size
            if size > 0:
                assert isinstance(t.tolist(), list)
                assert len(t.tolist()) == size

    def test_arange_tensor_creation(self):
        """Test creating range tensors."""
        # Test range tensor
        t = Tensor.arange(5)
        assert len(t) == 5
        values = t.tolist()
        expected = [0.0, 1.0, 2.0, 3.0, 4.0]
        assert values == expected

    def test_indexing(self):
        """Test tensor indexing."""
        t = Tensor.arange(5)
        
        # Test positive indexing
        assert t[0].item() == 0.0
        assert t[2].item() == 2.0
        assert t[4].item() == 4.0
        
        # Test negative indexing
        assert t[-1].item() == 4.0
        assert t[-2].item() == 3.0

    def test_slicing(self):
        """Test tensor slicing."""
        t = Tensor.arange(10)
        
        # Test basic slicing
        s1 = t[2:5]
        assert s1.tolist() == [2.0, 3.0, 4.0]
        
        # Test slicing with step
        s2 = t[::2]
        assert s2.tolist() == [0.0, 2.0, 4.0, 6.0, 8.0]
        
        # Test slicing with start, stop, step
        s3 = t[1:8:2]
        assert s3.tolist() == [1.0, 3.0, 5.0, 7.0]

    def test_arithmetic_addf(self):
        """Test adding a float to a tensor."""
        t = Tensor.arange(3)  # [0.0, 1.0, 2.0]
        t_plus_5 = t.addf(5.0)
        
        expected = [5.0, 6.0, 7.0]
        assert t_plus_5.tolist() == expected
        
        # Original tensor should be unchanged
        assert t.tolist() == [0.0, 1.0, 2.0]

    def test_arithmetic_add_tensors(self):
        """Test adding two tensors."""
        t1 = Tensor.arange(3)  # [0.0, 1.0, 2.0]
        t2 = Tensor.arange(3)  # [0.0, 1.0, 2.0]
        
        result = t1.add(t2)
        expected = [0.0, 2.0, 4.0]
        assert result.tolist() == expected
        
        # Original tensors should be unchanged
        assert t1.tolist() == [0.0, 1.0, 2.0]
        assert t2.tolist() == [0.0, 1.0, 2.0]

    def test_string_representation(self):
        """Test string representation of tensors."""
        t = Tensor.arange(3)
        str_repr = str(t)
        
        # Should contain the values
        assert "0.0" in str_repr
        assert "1.0" in str_repr
        assert "2.0" in str_repr

    def test_item_method(self):
        """Test the item() method for single-element tensors."""
        # This should work for tensors with a single element
        t = Tensor.arange(1)
        assert t.item() == 0.0

    def test_len_method(self):
        """Test the len() function on tensors."""
        assert len(Tensor.empty(0)) == 0
        assert len(Tensor.empty(1)) == 1
        assert len(Tensor.arange(10)) == 10

    def test_memory_management(self):
        """Test that we can create and destroy many tensors without issues."""
        # This tests that memory management works correctly
        for i in range(100):
            t = Tensor.arange(i % 10 + 1)
            _ = t.addf(float(i))
            # Tensors should be automatically cleaned up

    def test_edge_cases(self):
        """Test edge cases and error conditions."""
        # Empty tensor
        empty = Tensor.empty(0)
        assert len(empty) == 0
        
        # Single element tensor
        single = Tensor.arange(1)
        assert len(single) == 1
        assert single[0].item() == 0.0


class TestTensorErrors:
    """Test error conditions and invalid inputs."""

    def test_invalid_index_type(self):
        """Test that invalid index types raise appropriate errors."""
        t = Tensor.arange(5)
        
        with pytest.raises(TypeError):
            _ = t["invalid"]
        
        with pytest.raises(TypeError):
            _ = t[1.5]

    def test_invalid_arithmetic_types(self):
        """Test that invalid arithmetic operations raise errors."""
        t = Tensor.arange(3)
        
        with pytest.raises(TypeError):
            t.add("invalid")
        
        with pytest.raises(TypeError):
            t.add(123)  # Should be a Tensor, not an int


if __name__ == "__main__":
    # Allow running this test file directly
    pytest.main([__file__, "-v"])