"""
Simple tests for tensor1d functionality - no external dependencies needed.
"""
import sys
import os

# Add the project root to the path so we can import tensor
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from tensor.tensor1d import Tensor


def test_basic_functionality():
    """Test basic tensor functionality."""
    print("Running basic functionality tests...")
    
    # Test 1: Empty tensor creation
    print("  * Testing empty tensor creation...")
    t1 = Tensor.empty(3)
    assert len(t1) == 3
    print(f"    Created empty tensor: {t1}")
    
    # Test 2: Range tensor creation
    print("  * Testing range tensor creation...")
    t2 = Tensor.arange(5)
    assert len(t2) == 5
    assert t2.tolist() == [0.0, 1.0, 2.0, 3.0, 4.0]
    print(f"    Created range tensor: {t2}")
    
    # Test 3: Indexing
    print("  * Testing indexing...")
    assert t2[0].item() == 0.0
    assert t2[2].item() == 2.0
    assert t2[-1].item() == 4.0
    print("    Indexing works correctly")
    
    # Test 4: Slicing
    print("  * Testing slicing...")
    s1 = t2[1:4]
    assert s1.tolist() == [1.0, 2.0, 3.0]
    
    s2 = t2[::2]
    assert s2.tolist() == [0.0, 2.0, 4.0]
    print("    Slicing works correctly")
    
    # Test 5: Arithmetic
    print("  * Testing arithmetic...")
    t3 = t2.addf(5.0)
    assert t3.tolist() == [5.0, 6.0, 7.0, 8.0, 9.0]
    
    t4 = t2.add(t2)
    assert t4.tolist() == [0.0, 2.0, 4.0, 6.0, 8.0]
    print("    Arithmetic operations work correctly")
    
    print("All tests passed!")


def test_error_conditions():
    """Test error conditions."""
    print("Testing error conditions...")
    
    t = Tensor.arange(3)
    
    # Test invalid index types
    try:
        _ = t["invalid"]
        assert False, "Should have raised TypeError"
    except TypeError:
        print("  * Invalid string index correctly raises TypeError")
    
    # Test invalid arithmetic
    try:
        t.add("invalid")
        assert False, "Should have raised TypeError"
    except TypeError:
        print("  * Invalid arithmetic correctly raises TypeError")
    
    print("Error condition tests passed!")


def main():
    """Run all tests."""
    print("Starting tensor1d test suite...")
    print("=" * 50)
    
    try:
        test_basic_functionality()
        print()
        test_error_conditions()
        print()
        print("=" * 50)
        print("ALL TESTS PASSED!")
        return 0
    except Exception as e:
        print(f"Test failed: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    exit(main())