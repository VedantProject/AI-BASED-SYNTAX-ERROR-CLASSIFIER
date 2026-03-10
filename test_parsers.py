"""Quick test script to verify parser fixes"""
import sys
from main.controller import ParserController

def test_invalid_c():
    print("\n=== Testing Invalid C File ===")
    controller = ParserController()
    result = controller.parse_file("test_samples/invalid_test.c")
    controller.display_result(result)
    return result.get('success') is False

def test_invalid_java():
    print("\n=== Testing Invalid Java File ===")
    controller = ParserController()
    result = controller.parse_file("test_samples/InvalidTest.java")
    controller.display_result(result)
    return result.get('success') is False

def test_invalid_python():
    print("\n=== Testing Invalid Python File ===")
    controller = ParserController()
    result = controller.parse_file("test_samples/invalid_test.py")
    controller.display_result(result)
    return result.get('success') is False

if __name__ == "__main__":
    print("=" * 70)
    print("PARSER ROBUSTNESS TEST")
    print("=" * 70)
    
    tests = [
        ("Invalid C", test_invalid_c),
        ("Invalid Java", test_invalid_java),
        ("Invalid Python", test_invalid_python)
    ]
    
    passed = 0
    for name, test_func in tests:
        try:
            if test_func():
                print(f"✓ {name} test passed (detected errors correctly)")
                passed += 1
            else:
                print(f"✗ {name} test failed (should have detected errors)")
        except Exception as e:
            print(f"✗ {name} test crashed: {e}")
    
    print("\n" + "=" * 70)
    print(f"Results: {passed}/{len(tests)} tests passed")
    print("=" * 70)
    
    sys.exit(0 if passed == len(tests) else 1)
