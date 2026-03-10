"""
Demo Script
Demonstrates the capabilities of the Multi-Language Parser Framework
"""

import os
import sys

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from main.controller import ParserController
from dataset_generator import DatasetGenerator


def create_test_files():
    """Create sample test files for demonstration"""
    test_dir = "test_samples"
    os.makedirs(test_dir, exist_ok=True)
    
    # Valid C file
    valid_c = os.path.join(test_dir, "valid_test.c")
    with open(valid_c, 'w') as f:
        f.write("""#include <stdio.h>

int factorial(int n) {
    if (n <= 1) {
        return 1;
    }
    return n * factorial(n - 1);
}

int main() {
    int num = 5;
    printf("Factorial of %d is %d\\n", num, factorial(num));
    return 0;
}
""")
    
    # Invalid C file (missing semicolon)
    invalid_c = os.path.join(test_dir, "invalid_test.c")
    with open(invalid_c, 'w') as f:
        f.write("""#include <stdio.h>

int main() {
    int x = 10
    int y = 20;
    printf("Sum: %d\\n", x + y);
    return 0;
}
""")
    
    # Valid Java file
    valid_java = os.path.join(test_dir, "ValidTest.java")
    with open(valid_java, 'w') as f:
        f.write("""public class ValidTest {
    public static int add(int a, int b) {
        return a + b;
    }
    
    public static void main(String[] args) {
        int result = add(5, 10);
        System.out.println("Result: " + result);
    }
}
""")
    
    # Invalid Java file (missing brace)
    invalid_java = os.path.join(test_dir, "InvalidTest.java")
    with open(invalid_java, 'w') as f:
        f.write("""public class InvalidTest {
    public static void main(String[] args) {
        if (true) {
            System.out.println("Hello");
        
    }
}
""")
    
    # Valid Python file
    valid_python = os.path.join(test_dir, "valid_test.py")
    with open(valid_python, 'w') as f:
        f.write("""def fibonacci(n):
    if n <= 1:
        return n
    return fibonacci(n-1) + fibonacci(n-2)

if __name__ == "__main__":
    for i in range(10):
        print(f"fib({i}) = {fibonacci(i)}")
""")
    
    # Invalid Python file (indentation error)
    invalid_python = os.path.join(test_dir, "invalid_test.py")
    with open(invalid_python, 'w') as f:
        f.write("""def greet(name):
    message = f"Hello, {name}!"
  print(message)

greet("World")
""")
    
    return test_dir


def demo_single_file_parsing():
    """Demonstrate single file parsing"""
    print("\n" + "=" * 70)
    print("DEMO 1: Single File Parsing")
    print("=" * 70)
    
    test_dir = create_test_files()
    controller = ParserController()
    
    # Parse valid C file
    print("\n--- Parsing Valid C File ---")
    result = controller.parse_file(os.path.join(test_dir, "valid_test.c"))
    controller.display_result(result)
    
    # Parse invalid C file
    print("\n--- Parsing Invalid C File (Missing Semicolon) ---")
    result = controller.parse_file(os.path.join(test_dir, "invalid_test.c"))
    controller.display_result(result)
    
    # Parse invalid Python file
    print("\n--- Parsing Invalid Python File (Indentation Error) ---")
    result = controller.parse_file(os.path.join(test_dir, "invalid_test.py"))
    controller.display_result(result)


def demo_batch_processing():
    """Demonstrate batch processing"""
    print("\n" + "=" * 70)
    print("DEMO 2: Batch Processing")
    print("=" * 70)
    
    test_dir = create_test_files()
    controller = ParserController()
    
    # Process all test files
    print("\nProcessing all test files...")
    result = controller.parse_batch(test_dir, output_dir="results/demo")
    controller.display_batch_summary(result)


def demo_dataset_generation():
    """Demonstrate dataset generation"""
    print("\n" + "=" * 70)
    print("DEMO 3: Dataset Generation")
    print("=" * 70)
    
    generator = DatasetGenerator("datasets")
    
    # Generate small dataset for demo
    print("\nGenerating small dataset (50 files per language)...")
    generator.generate_c_dataset(25, 25)
    generator.generate_java_dataset(25, 25)
    generator.generate_python_dataset(25, 25)
    
    print("\n✓ Dataset generation complete!")


def demo_batch_on_dataset():
    """Demonstrate batch processing on generated dataset"""
    print("\n" + "=" * 70)
    print("DEMO 4: Batch Processing on Generated Dataset")
    print("=" * 70)
    
    controller = ParserController()
    
    # Process C dataset
    if os.path.exists("datasets/c"):
        print("\n--- Processing C Dataset ---")
        result = controller.parse_batch("datasets/c", language="c", 
                                       output_dir="results/batch_c")
        controller.display_batch_summary(result)
    
    # Process Python dataset
    if os.path.exists("datasets/python"):
        print("\n--- Processing Python Dataset ---")
        result = controller.parse_batch("datasets/python", language="python",
                                       output_dir="results/batch_python")
        controller.display_batch_summary(result)


def main():
    """Run all demos"""
    print("\n" + "=" * 70)
    print("MULTI-LANGUAGE PARSER FRAMEWORK - DEMONSTRATION")
    print("AI-Based Syntax Error Classification - Phase 1")
    print("=" * 70)
    
    try:
        # Demo 1: Single file parsing
        demo_single_file_parsing()
        
        # Demo 2: Batch processing on test files
        demo_batch_processing()
        
        # Demo 3: Dataset generation
        demo_dataset_generation()
        
        # Demo 4: Batch processing on generated dataset
        demo_batch_on_dataset()
        
        print("\n" + "=" * 70)
        print("DEMONSTRATION COMPLETE")
        print("=" * 70)
        print("\nAll results have been saved to the 'results/' directory")
        print("Generated datasets are in the 'datasets/' directory")
        print("\nYou can now:")
        print("  - Run 'python main.py --help' to see all options")
        print("  - Run 'python dataset_generator.py --help' for dataset options")
        print("  - Examine results in the 'results/' directory")
        print("  - Test with your own source files")
        
    except Exception as e:
        print(f"\nError during demonstration: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
