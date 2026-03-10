"""
Dataset Generator
Generates large datasets of valid and invalid source code for testing
"""

import os
import random
import json
from typing import List, Dict
from main.utils import ensure_dir, write_file, write_json
from main.controller import ParserController


class DatasetGenerator:
    """Generate synthetic code datasets for parser testing"""
    
    def __init__(self, output_dir: str = "datasets"):
        self.output_dir = output_dir
        ensure_dir(output_dir)
    
    def generate_all(self, valid_count: int = 500, invalid_count: int = 500, 
                     run_parsing: bool = True):
        """Generate datasets for all supported languages"""
        print(f"\nGenerating datasets...")
        print(f"Valid samples per language: {valid_count}")
        print(f"Invalid samples per language: {invalid_count}")
        
        self.generate_c_dataset(valid_count, invalid_count)
        self.generate_java_dataset(valid_count, invalid_count)
        self.generate_python_dataset(valid_count, invalid_count)
        
        print(f"\n[OK] Dataset generation complete!")
        print(f"  Location: {self.output_dir}")
        
        # Automatically run batch parsing if requested
        if run_parsing:
            print(f"\n{'='*70}")
            print("STARTING BATCH PARSING ON GENERATED DATASETS")
            print(f"{'='*70}")
            self.parse_all_datasets()
    
    # ============= C/C++ Dataset =============
    
    def generate_c_dataset(self, valid_count: int, invalid_count: int):
        """Generate C/C++ code samples"""
        lang_dir = os.path.join(self.output_dir, "c")
        valid_dir = os.path.join(lang_dir, "valid")
        invalid_dir = os.path.join(lang_dir, "invalid")
        
        ensure_dir(valid_dir)
        ensure_dir(invalid_dir)
        
        print(f"\nGenerating C/C++ dataset...")
        
        # Valid samples
        for i in range(valid_count):
            code = self._generate_valid_c_code(i)
            filepath = os.path.join(valid_dir, f"valid_{i:04d}.c")
            write_file(filepath, code)
        
        # Invalid samples
        for i in range(invalid_count):
            code, error_type = self._generate_invalid_c_code(i)
            filepath = os.path.join(invalid_dir, f"invalid_{error_type}_{i:04d}.c")
            write_file(filepath, code)
        
        print(f"  [OK] Generated {valid_count} valid + {invalid_count} invalid C files")
    
    def _generate_valid_c_code(self, seed: int) -> str:
        """Generate valid C code"""
        random.seed(seed)
        templates = [
            # Simple function
            """#include <stdio.h>

int add(int a, int b) {
    return a + b;
}

int main() {
    int x = 5;
    int y = 10;
    int result = add(x, y);
    printf("Result: %d\\n", result);
    return 0;
}
""",
            # With loops
            """#include <stdio.h>

int factorial(int n) {
    int result = 1;
    for (int i = 1; i <= n; i++) {
        result *= i;
    }
    return result;
}

int main() {
    int num = 5;
    printf("Factorial of %d is %d\\n", num, factorial(num));
    return 0;
}
""",
            # With conditionals
            """#include <stdio.h>

int max(int a, int b) {
    if (a > b) {
        return a;
    } else {
        return b;
    }
}

int main() {
    int x = 10;
    int y = 20;
    printf("Max: %d\\n", max(x, y));
    return 0;
}
""",
            # Array operations
            """#include <stdio.h>

int sum_array(int arr[], int size) {
    int sum = 0;
    for (int i = 0; i < size; i++) {
        sum += arr[i];
    }
    return sum;
}

int main() {
    int numbers[] = {1, 2, 3, 4, 5};
    int size = 5;
    printf("Sum: %d\\n", sum_array(numbers, size));
    return 0;
}
""",
            # Struct usage
            """#include <stdio.h>

struct Point {
    int x;
    int y;
};

void print_point(struct Point p) {
    printf("Point(%d, %d)\\n", p.x, p.y);
}

int main() {
    struct Point p1;
    p1.x = 10;
    p1.y = 20;
    print_point(p1);
    return 0;
}
"""
        ]
        
        return random.choice(templates)
    
    def _generate_invalid_c_code(self, seed: int) -> tuple:
        """Generate invalid C code with specific error types"""
        random.seed(seed)
        
        error_generators = [
            ("missing_semicolon", lambda: """#include <stdio.h>

int main() {
    int x = 5
    int y = 10;
    return 0;
}
"""         ),
            ("missing_brace", lambda: """#include <stdio.h>

int main() {
    int x = 5;
    if (x > 0) {
        printf("Positive\\n");
    
    return 0;
}
"""),
            ("missing_paren", lambda: """#include <stdio.h>

int add(int a, int b {
    return a + b;
}

int main() {
    return 0;
}
"""),
            ("invalid_declaration", lambda: """#include <stdio.h>

int main() {
    int;
    x = 5;
    return 0;
}
"""),
            ("missing_return_type", lambda: """#include <stdio.h>

main() {
    printf("Hello\\n");
    return 0;
}
"""),
            ("unmatched_delimiter", lambda: """#include <stdio.h>

int main() {
    int arr[5] = {1, 2, 3, 4, 5;
    return 0;
}
"""),
        ]
        
        error_type, generator = random.choice(error_generators)
        return generator(), error_type
    
    # ============= Java Dataset =============
    
    def generate_java_dataset(self, valid_count: int, invalid_count: int):
        """Generate Java code samples"""
        lang_dir = os.path.join(self.output_dir, "java")
        valid_dir = os.path.join(lang_dir, "valid")
        invalid_dir = os.path.join(lang_dir, "invalid")
        
        ensure_dir(valid_dir)
        ensure_dir(invalid_dir)
        
        print(f"Generating Java dataset...")
        
        # Valid samples
        for i in range(valid_count):
            code = self._generate_valid_java_code(i)
            filepath = os.path.join(valid_dir, f"Valid{i:04d}.java")
            write_file(filepath, code)
        
        # Invalid samples
        for i in range(invalid_count):
            code, error_type = self._generate_invalid_java_code(i)
            filepath = os.path.join(invalid_dir, f"Invalid_{error_type}_{i:04d}.java")
            write_file(filepath, code)
        
        print(f"  [OK] Generated {valid_count} valid + {invalid_count} invalid Java files")
    
    def _generate_valid_java_code(self, seed: int) -> str:
        """Generate valid Java code"""
        random.seed(seed)
        templates = [
            # Simple class
            f"""public class Valid{seed:04d} {{
    public static void main(String[] args) {{
        int x = 5;
        int y = 10;
        System.out.println("Sum: " + (x + y));
    }}
}}
""",
            # With methods
            f"""public class Valid{seed:04d} {{
    public static int add(int a, int b) {{
        return a + b;
    }}
    
    public static void main(String[] args) {{
        int result = add(5, 10);
        System.out.println("Result: " + result);
    }}
}}
""",
            # With loops
            f"""public class Valid{seed:04d} {{
    public static void main(String[] args) {{
        for (int i = 0; i < 10; i++) {{
            System.out.println("Count: " + i);
        }}
    }}
}}
""",
            # With class and objects
            f"""public class Valid{seed:04d} {{
    private int value;
    
    public Valid{seed:04d}(int value) {{
        this.value = value;
    }}
    
    public int getValue() {{
        return value;
    }}
    
    public static void main(String[] args) {{
        Valid{seed:04d} obj = new Valid{seed:04d}(42);
        System.out.println("Value: " + obj.getValue());
    }}
}}
""",
            # With conditionals
            f"""public class Valid{seed:04d} {{
    public static int max(int a, int b) {{
        if (a > b) {{
            return a;
        }} else {{
            return b;
        }}
    }}
    
    public static void main(String[] args) {{
        System.out.println("Max: " + max(10, 20));
    }}
}}
"""
        ]
        
        return random.choice(templates)
    
    def _generate_invalid_java_code(self, seed: int) -> tuple:
        """Generate invalid Java code"""
        random.seed(seed)
        
        error_generators = [
            ("missing_semicolon", lambda: f"""public class Invalid_{seed:04d} {{
    public static void main(String[] args) {{
        int x = 5
        int y = 10;
    }}
}}
"""),
            ("missing_brace", lambda: f"""public class Invalid_{seed:04d} {{
    public static void main(String[] args) {{
        if (true) {{
            System.out.println("Hello");
        
    }}
}}
"""),
            ("missing_paren", lambda: f"""public class Invalid_{seed:04d} {{
    public static void main(String[] args {{
        System.out.println("Hello");
    }}
}}
"""),
            ("invalid_declaration", lambda: f"""public class Invalid_{seed:04d} {{
    public static void main(String[] args) {{
        int;
        x = 5;
    }}
}}
"""),
            ("missing_return_type", lambda: f"""public class Invalid_{seed:04d} {{
    public static getValue() {{
        return 42;
    }}
}}
"""),
            ("missing_class_name", lambda: f"""public class {{
    public static void main(String[] args) {{
        System.out.println("Hello");
    }}
}}
"""),
        ]
        
        error_type, generator = random.choice(error_generators)
        return generator(), error_type
    
    # ============= Python Dataset =============
    
    def generate_python_dataset(self, valid_count: int, invalid_count: int):
        """Generate Python code samples"""
        lang_dir = os.path.join(self.output_dir, "python")
        valid_dir = os.path.join(lang_dir, "valid")
        invalid_dir = os.path.join(lang_dir, "invalid")
        
        ensure_dir(valid_dir)
        ensure_dir(invalid_dir)
        
        print(f"Generating Python dataset...")
        
        # Valid samples
        for i in range(valid_count):
            code = self._generate_valid_python_code(i)
            filepath = os.path.join(valid_dir, f"valid_{i:04d}.py")
            write_file(filepath, code)
        
        # Invalid samples
        for i in range(invalid_count):
            code, error_type = self._generate_invalid_python_code(i)
            filepath = os.path.join(invalid_dir, f"invalid_{error_type}_{i:04d}.py")
            write_file(filepath, code)
        
        print(f"  [OK] Generated {valid_count} valid + {invalid_count} invalid Python files")
    
    def _generate_valid_python_code(self, seed: int) -> str:
        """Generate valid Python code"""
        random.seed(seed)
        templates = [
            # Simple function
            """def add(a, b):
    return a + b

if __name__ == "__main__":
    x = 5
    y = 10
    result = add(x, y)
    print(f"Result: {result}")
""",
            # With loops
            """def factorial(n):
    result = 1
    for i in range(1, n + 1):
        result *= i
    return result

if __name__ == "__main__":
    num = 5
    print(f"Factorial of {num} is {factorial(num)}")
""",
            # With class
            """class Calculator:
    def __init__(self):
        self.result = 0
    
    def add(self, x, y):
        self.result = x + y
        return self.result
    
    def get_result(self):
        return self.result

if __name__ == "__main__":
    calc = Calculator()
    calc.add(5, 10)
    print(f"Result: {calc.get_result()}")
""",
            # List operations
            """def sum_list(numbers):
    total = 0
    for num in numbers:
        total += num
    return total

if __name__ == "__main__":
    nums = [1, 2, 3, 4, 5]
    print(f"Sum: {sum_list(nums)}")
""",
            # Conditionals
            """def max_value(a, b):
    if a > b:
        return a
    else:
        return b

if __name__ == "__main__":
    print(f"Max: {max_value(10, 20)}")
"""
        ]
        
        return random.choice(templates)
    
    def _generate_invalid_python_code(self, seed: int) -> tuple:
        """Generate invalid Python code"""
        random.seed(seed)
        
        error_generators = [
            ("missing_colon", lambda: """def add(a, b)
    return a + b

print(add(5, 10))
"""),
            ("indentation_error", lambda: """def add(a, b):
    return a + b

if __name__ == "__main__":
x = 5
    y = 10
    print(add(x, y))
"""),
            ("missing_paren", lambda: """def add(a, b):
    return a + b

if __name__ == "__main__":
    result = add(5, 10
    print(result)
"""),
            ("missing_bracket", lambda: """def process_list():
    numbers = [1, 2, 3, 4, 5
    return sum(numbers)

print(process_list())
"""),
            ("invalid_syntax", lambda: """def calculate():
    x = 5
    y = 10
    return x ++ y

print(calculate())
"""),
            ("incomplete_statement", lambda: """def test():
    x = 
    return x

print(test())
"""),
        ]
        
        error_type, generator = random.choice(error_generators)
        return generator(), error_type
    
    # ============= Batch Parsing & Reporting =============
    
    def parse_all_datasets(self):
        """Run batch parsing on all generated datasets and create final report"""
        controller = ParserController()
        final_results = {}
        
        # Parse each language dataset
        languages = ['c', 'java', 'python']
        
        for lang in languages:
            lang_dir = os.path.join(self.output_dir, lang)
            
            if not os.path.exists(lang_dir):
                print(f"\nSkipping {lang.upper()}: Dataset not found")
                continue
            
            print(f"\n{'='*70}")
            print(f"PARSING {lang.upper()} DATASET")
            print(f"{'='*70}")
            
            # Parse the dataset
            output_dir = os.path.join('results', f'batch_{lang}')
            result = controller.parse_batch(lang_dir, language=lang, output_dir=output_dir)
            
            # Store results
            final_results[lang] = result
            
            # Display summary
            controller.display_batch_summary(result)
        
        # Generate final comprehensive report
        self.generate_final_report(final_results)
    
    def generate_final_report(self, results: Dict[str, Dict]):
        """Generate comprehensive final report from all language results"""
        print(f"\n{'='*70}")
        print("GENERATING FINAL COMPREHENSIVE REPORT")
        print(f"{'='*70}")
        
        final_dir = os.path.join('results', 'final')
        ensure_dir(final_dir)
        
        # Aggregate statistics
        total_stats = {
            'total_files': 0,
            'successful_parses': 0,
            'failed_parses': 0,
            'files_with_errors': 0,
            'total_errors': 0,
            'by_language': {}
        }
        
        error_categories = {}
        
        for lang, result in results.items():
            # Language-specific stats
            error_summary = result.get('error_summary', {})
            lang_stats = {
                'total_files': result.get('total_files', 0),
                'successful_parses': result.get('successful_parses', 0),
                'failed_parses': result.get('failed_parses', 0),
                'files_with_errors': result.get('files_with_syntax_errors', 0),
                'total_errors': error_summary.get('total_errors', 0),
                'error_categories': error_summary.get('by_category', {})
            }
            
            total_stats['by_language'][lang] = lang_stats
            
            # Aggregate totals
            total_stats['total_files'] += lang_stats['total_files']
            total_stats['successful_parses'] += lang_stats['successful_parses']
            total_stats['failed_parses'] += lang_stats['failed_parses']
            total_stats['files_with_errors'] += lang_stats['files_with_errors']
            total_stats['total_errors'] += lang_stats['total_errors']
            
            # Merge error categories
            for category, count in lang_stats['error_categories'].items():
                error_categories[category] = error_categories.get(category, 0) + count
        
        total_stats['error_categories'] = error_categories
        
        # Create final report structure
        final_report = {
            'summary': total_stats,
            'language_details': results
        }
        
        # Save JSON report
        json_file = os.path.join(final_dir, 'final_report.json')
        write_json(json_file, final_report)
        
        # Generate text summary
        summary_file = os.path.join(final_dir, 'summary.txt')
        summary_text = self._format_final_summary(total_stats)
        with open(summary_file, 'w', encoding='utf-8') as f:
            f.write(summary_text)
        
        print(f"\n[OK] Final reports saved to: {final_dir}")
        print(f"  - {json_file}")
        print(f"  - {summary_file}")
        
        # Print final summary to console
        print(f"\n{'='*70}")
        print("FINAL COMPREHENSIVE SUMMARY")
        print(f"{'='*70}")
        print(summary_text)
    
    def _format_final_summary(self, stats: Dict) -> str:
        """Format final summary as text"""
        lines = []
        lines.append("=" * 60)
        lines.append("FINAL PARSING REPORT - ALL LANGUAGES")
        lines.append("=" * 60)
        lines.append("")
        
        # Overall statistics
        lines.append("OVERALL STATISTICS:")
        lines.append(f"  Total Files Processed: {stats['total_files']}")
        lines.append(f"  Successful Parses: {stats['successful_parses']} ({stats['successful_parses']/max(stats['total_files'],1)*100:.1f}%)")
        lines.append(f"  Failed Parses: {stats['failed_parses']} ({stats['failed_parses']/max(stats['total_files'],1)*100:.1f}%)")
        lines.append(f"  Files with Syntax Errors: {stats['files_with_errors']}")
        lines.append(f"  Total Errors Found: {stats['total_errors']}")
        lines.append("")
        
        # By language
        lines.append("BREAKDOWN BY LANGUAGE:")
        lines.append("")
        
        for lang, lang_stats in stats['by_language'].items():
            lines.append(f"  {lang.upper()}:")
            lines.append(f"    Files: {lang_stats['total_files']}")
            lines.append(f"    Successful: {lang_stats['successful_parses']}")
            lines.append(f"    Failed: {lang_stats['failed_parses']}")
            lines.append(f"    With Errors: {lang_stats['files_with_errors']}")
            lines.append(f"    Total Errors: {lang_stats['total_errors']}")
            
            if lang_stats['error_categories']:
                lines.append(f"    Error Categories:")
                for category, count in sorted(lang_stats['error_categories'].items(), 
                                             key=lambda x: x[1], reverse=True):
                    lines.append(f"      - {category}: {count}")
            lines.append("")
        
        # Overall error categories
        if stats['error_categories']:
            lines.append("OVERALL ERROR CATEGORIES:")
            for category, count in sorted(stats['error_categories'].items(), 
                                         key=lambda x: x[1], reverse=True):
                percentage = count / max(stats['total_errors'], 1) * 100
                lines.append(f"  - {category}: {count} ({percentage:.1f}%)")
            lines.append("")
        
        lines.append("=" * 60)
        
        return "\n".join(lines)


def main():
    """Main entry point for dataset generation"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Generate parser test datasets")
    parser.add_argument('--language', choices=['c', 'java', 'python', 'all'], 
                       default='all', help='Language to generate')
    parser.add_argument('--valid', type=int, default=500, 
                       help='Number of valid samples per language')
    parser.add_argument('--invalid', type=int, default=500,
                       help='Number of invalid samples per language')
    parser.add_argument('--output', default='datasets',
                       help='Output directory')
    parser.add_argument('--no-parse', action='store_true',
                       help='Skip automatic batch parsing after generation')
    
    args = parser.parse_args()
    
    generator = DatasetGenerator(args.output)
    run_parsing = not args.no_parse
    
    if args.language == 'all':
        generator.generate_all(args.valid, args.invalid, run_parsing=run_parsing)
    elif args.language == 'c':
        generator.generate_c_dataset(args.valid, args.invalid)
        if run_parsing:
            print(f"\n{'='*70}")
            print("STARTING BATCH PARSING")
            print(f"{'='*70}")
            generator.parse_all_datasets()
    elif args.language == 'java':
        generator.generate_java_dataset(args.valid, args.invalid)
        if run_parsing:
            print(f"\n{'='*70}")
            print("STARTING BATCH PARSING")
            print(f"{'='*70}")
            generator.parse_all_datasets()
    elif args.language == 'python':
        generator.generate_python_dataset(args.valid, args.invalid)
        if run_parsing:
            print(f"\n{'='*70}")
            print("STARTING BATCH PARSING")
            print(f"{'='*70}")
            generator.parse_all_datasets()


if __name__ == "__main__":
    main()
