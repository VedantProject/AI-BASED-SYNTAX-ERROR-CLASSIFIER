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
                     python_valid_count: int = 5000, python_invalid_count: int = 5000,
                     run_parsing: bool = True):
        """Generate datasets for all supported languages.

        C and Java use valid_count / invalid_count (default 500 each).
        Python uses python_valid_count / python_invalid_count (default 5000 each)
        so the Python ML model trains on 10 000 samples total.
        """
        print(f"\nGenerating datasets...")
        print(f"C / Java  – valid: {valid_count}, invalid: {invalid_count}")
        print(f"Python    – valid: {python_valid_count}, invalid: {python_invalid_count}")

        self.generate_c_dataset(valid_count, invalid_count)
        self.generate_java_dataset(valid_count, invalid_count)
        self.generate_python_dataset(python_valid_count, python_invalid_count)
        
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
    
    def generate_python_dataset(self, valid_count: int = 5000, invalid_count: int = 5000):
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
        """Generate valid Python code with 30 parameterised templates."""
        random.seed(seed)

        # ── random pools ──────────────────────────────────────────────────
        var_pool  = ['x', 'y', 'z', 'a', 'b', 'n', 'm', 'val', 'count',
                     'total', 'result', 'data', 'item', 'temp', 'num', 'res',
                     'acc', 'diff', 'prod', 'size']
        func_pool = ['compute', 'process', 'analyze', 'evaluate', 'transform',
                     'convert', 'check', 'find', 'generate', 'solve', 'run',
                     'build', 'collect', 'merge', 'filter_vals']
        cls_pool  = ['Calculator', 'Processor', 'Manager', 'Handler',
                     'Analyzer', 'Builder', 'Scanner', 'Tracker', 'Engine', 'Worker']
        ops       = ['+', '-', '*']
        str_pool  = ['hello', 'world', 'test', 'data', 'python',
                     'value', 'item', 'record', 'entry']

        v     = random.sample(var_pool, 6)
        v1, v2, v3, v4, v5, v6 = v
        fn    = random.choice(func_pool)
        fn2   = random.choice(func_pool)
        cn    = random.choice(cls_pool)
        op    = random.choice(ops)
        n1    = random.randint(2, 50)
        n2    = random.randint(2, 50)
        n3    = random.randint(2, 10)
        n4    = random.randint(1, 20)
        s1    = random.choice(str_pool)
        lst   = [random.randint(1, 99) for _ in range(n3 + 2)]
        lst5  = lst[:5]

        templates = [
            # 1. Simple arithmetic function
            f"""def {fn}({v1}, {v2}):
    return {v1} {op} {v2}

result = {fn}({n1}, {n2})
print(f"Result: {{result}}")
""",
            # 2. For-loop range accumulation
            f"""def sum_range({v1}, {v2}):
    {v3} = 0
    for i in range({v1}, {v2} + 1):
        {v3} += i
    return {v3}

print(sum_range({n1}, {n1 + n3}))
""",
            # 3. While-loop countdown
            f"""def countdown({v1}):
    results = []
    while {v1} > 0:
        results.append({v1})
        {v1} -= 1
    return results

print(countdown({n3}))
""",
            # 4. Recursive factorial
            f"""def factorial({v1}):
    if {v1} <= 1:
        return 1
    return {v1} * factorial({v1} - 1)

print(f"factorial({n3}) = {{factorial({n3})}}")
""",
            # 5. List sum with for-loop
            f"""def {fn}(numbers):
    {v1} = 0
    for num in numbers:
        {v1} += num
    return {v1}

data = {lst5}
print(f"Total: {{{fn}(data)}}")
""",
            # 6. Linear max search
            f"""def find_max(items):
    {v1} = items[0]
    for item in items[1:]:
        if item > {v1}:
            {v1} = item
    return {v1}

print(find_max({sorted(lst5)}))
""",
            # 7. Linear min search
            f"""def find_min(items):
    {v1} = items[0]
    for item in items[1:]:
        if item < {v1}:
            {v1} = item
    return {v1}

print(find_min({sorted(lst5, reverse=True)}))
""",
            # 8. String greeting
            f"""def greet(name, {v1}):
    return f"Hello, {{name}}! Count: {{{v1}}}"

msg = greet("{s1}", {n1})
print(msg)
""",
            # 9. Class with getter/setter
            f"""class {cn}:
    def __init__(self, {v1}):
        self._{v1} = {v1}

    def get_{v1}(self):
        return self._{v1}

    def set_{v1}(self, {v2}):
        self._{v1} = {v2}

obj = {cn}({n1})
print(obj.get_{v1}())
obj.set_{v1}({n2})
print(obj.get_{v1}())
""",
            # 10. Dict comprehension builder
            f"""def build_scores(names, values):
    return {{name: val for name, val in zip(names, values)}}

names = ["alice", "bob", "carol"]
vals  = [{n1}, {n2}, {n1 + n2}]
scores = build_scores(names, vals)
print(scores)
""",
            # 11. List comprehension – squares
            f"""def squares({v1}):
    return [i ** 2 for i in range({v1})]

print(squares({n3 + 2}))
""",
            # 12. List comprehension – filter even
            f"""def even_numbers({v1}):
    return [i for i in range({v1}) if i % 2 == 0]

print(even_numbers({n1}))
""",
            # 13. Fibonacci sequence
            f"""def fibonacci({v1}):
    if {v1} <= 0:
        return []
    if {v1} == 1:
        return [0]
    seq = [0, 1]
    for _ in range(2, {v1}):
        seq.append(seq[-1] + seq[-2])
    return seq

print(fibonacci({n3 + 2}))
""",
            # 14. Recursive power
            f"""def power({v1}, {v2}):
    if {v2} == 0:
        return 1
    return {v1} * power({v1}, {v2} - 1)

print(power({n2 % 10 + 2}, {n3 % 5 + 2}))
""",
            # 15. GCD (Euclidean)
            f"""def gcd({v1}, {v2}):
    while {v2} != 0:
        {v1}, {v2} = {v2}, {v1} % {v2}
    return {v1}

print(gcd({n1 * 2}, {n2}))
""",
            # 16. Sieve-style prime list
            f"""def is_prime({v1}):
    if {v1} < 2:
        return False
    for i in range(2, int({v1} ** 0.5) + 1):
        if {v1} % i == 0:
            return False
    return True

primes = [i for i in range(2, {n1 + 10}) if is_prime(i)]
print(primes)
""",
            # 17. Palindrome check
            f"""def is_palindrome({v1}):
    s = str({v1})
    return s == s[::-1]

for num in [{n1}, {n2}, 121, 131, {n3}]:
    print(f"{{num}}: {{is_palindrome(num)}}")
""",
            # 18. Average
            f"""def average(numbers):
    if not numbers:
        return 0
    return sum(numbers) / len(numbers)

data = {lst5}
print(f"Average: {{average(data):.2f}}")
""",
            # 19. String reversal
            f"""def reverse_string(s):
    return s[::-1]

words = ["{s1}", "python", "code", "test"]
for w in words:
    print(f"{{w}} -> {{reverse_string(w)}}")
""",
            # 20. Character frequency
            f"""def count_char(text, ch):
    return text.count(ch)

text = "{s1} {fn} python testing"
print(count_char(text, "{s1[0]}"))
""",
            # 21. Stack class
            f"""class Stack:
    def __init__(self):
        self._data = []

    def push(self, {v1}):
        self._data.append({v1})

    def pop(self):
        if self._data:
            return self._data.pop()
        return None

    def peek(self):
        return self._data[-1] if self._data else None

    def is_empty(self):
        return len(self._data) == 0

s = Stack()
for i in [{', '.join(str(e) for e in lst5)}]:
    s.push(i)
print(s.pop())
print(s.peek())
""",
            # 22. Bubble sort
            f"""def bubble_sort(arr):
    {v1} = arr[:]
    for i in range(len({v1}) - 1):
        for j in range(len({v1}) - i - 1):
            if {v1}[j] > {v1}[j + 1]:
                {v1}[j], {v1}[j + 1] = {v1}[j + 1], {v1}[j]
    return {v1}

print(bubble_sort({lst5}))
""",
            # 23. Generator (yield)
            f"""def range_gen(start, stop, step=1):
    current = start
    while current < stop:
        yield current
        current += step

print(list(range_gen({n1}, {n1 + n3 * 2}, {max(1, n3 % 4)})))
""",
            # 24. Closure / higher-order function
            f"""def make_adder({v1}):
    def adder({v2}):
        return {v1} + {v2}
    return adder

add_{n1} = make_adder({n1})
print(add_{n1}({n2}))
""",
            # 25. Exception handling
            f"""def safe_divide({v1}, {v2}):
    try:
        return {v1} / {v2}
    except ZeroDivisionError:
        return None

print(safe_divide({n1}, {n2}))
print(safe_divide({n1}, 0))
""",
            # 26. Multiple return values (min/max)
            f"""def min_max(numbers):
    return min(numbers), max(numbers)

lo, hi = min_max({lst5})
print(f"min={{lo}}, max={{hi}}")
""",
            # 27. String split/join/upper
            f"""def process_text(text):
    words = text.split()
    upper = [w.upper() for w in words]
    return " ".join(upper)

print(process_text("{s1} {fn} python code"))
""",
            # 28. Dictionary comprehension (square map)
            f"""def square_map(n):
    return {{i: i ** 2 for i in range(n)}}

d = square_map({n3 + 3})
for k, v in d.items():
    print(f"{{k}}^2 = {{v}}")
""",
            # 29. Two-pointer hash-map search
            f"""def two_sum(numbers, target):
    seen = {{}}
    for i, {v1} in enumerate(numbers):
        complement = target - {v1}
        if complement in seen:
            return (seen[complement], i)
        seen[{v1}] = i
    return None

result = two_sum({lst5}, {lst5[0] + lst5[-1]})
print(result)
""",
            # 30. Class with static counter
            f"""class {cn}:
    _count = 0

    def __init__(self, {v1}):
        self.value = {v1}
        {cn}._count += 1

    @staticmethod
    def get_count():
        return {cn}._count

    def double(self):
        return self.value * 2

objs = [{cn}(i) for i in range({n3})]
print(f"Created: {{{cn}.get_count()}} objects")
print([o.double() for o in objs])
""",
        ]

        return random.choice(templates)

    def _generate_invalid_python_code(self, seed: int) -> tuple:
        """Generate invalid Python code with 21 diverse error variants."""
        random.seed(seed)

        # ── random pools ──────────────────────────────────────────────────
        var_pool  = ['x', 'y', 'z', 'a', 'b', 'n', 'm', 'val', 'count', 'total']
        func_pool = ['compute', 'process', 'analyze', 'check', 'build', 'run']
        cls_pool  = ['Calculator', 'Processor', 'Manager', 'Handler', 'Engine']

        v  = random.sample(var_pool, 4)
        v1, v2, v3, v4 = v
        fn = random.choice(func_pool)
        cn = random.choice(cls_pool)
        n1 = random.randint(2, 50)
        n2 = random.randint(2, 50)
        n3 = random.randint(2, 8)

        error_generators = [
            # ── missing_colon (5 variants) ────────────────────────────────
            ("missing_colon", lambda: f"""def {fn}({v1}, {v2})
    return {v1} + {v2}

print({fn}({n1}, {n2}))
"""),
            ("missing_colon", lambda: f"""def check({v1}):
    if {v1} > 0
        return True
    return False

print(check({n1}))
"""),
            ("missing_colon", lambda: f"""for i in range({n3})
    print(i)
"""),
            ("missing_colon", lambda: f"""def {fn}({v1}):
    while {v1} > 0
        {v1} -= 1
    return {v1}

{fn}({n3})
"""),
            ("missing_colon", lambda: f"""class {cn}
    def __init__(self, {v1}):
        self.{v1} = {v1}
"""),

            # ── missing_paren (3 variants) ────────────────────────────────
            ("missing_paren", lambda: f"""def {fn}({v1}, {v2}):
    return {v1} + {v2}

result = {fn}({n1}, {n2}
print(result)
"""),
            ("missing_paren", lambda: f"""{v1} = {n1}
if ({v1} > 0:
    print("positive")
"""),
            ("missing_paren", lambda: f"""def compute({v1}):
    return (({v1} * 2) + {n2}

print(compute({n1}))
"""),

            # ── missing_bracket (3 variants) ──────────────────────────────
            ("missing_bracket", lambda: f"""numbers = [1, 2, 3, {n1}, {n2}
total = sum(numbers)
print(total)
"""),
            ("missing_bracket", lambda: f"""def {fn}():
    data = [{n1}, {n2}, {n3}
    return data

print({fn}())
"""),
            ("missing_bracket", lambda: f"""matrix = [[1, 2], [3, 4], [5, 6]
for row in matrix:
    print(row)
"""),

            # ── missing_brace (3 variants) ────────────────────────────────
            ("missing_brace", lambda: f"""config = {{"key": {n1}, "val": {n2}
print(config)
"""),
            ("missing_brace", lambda: f"""def {fn}():
    mapping = {{"{v1}": {n1}, "{v2}": {n2}
    return mapping

print({fn}())
"""),
            ("missing_brace", lambda: f"""scores = {{"alice": {n1}, "bob": {n2}, "carol": {n3}
for name, score in scores.items():
    print(name, score)
"""),

            # ── indentation_error (3 variants) ────────────────────────────
            ("indentation_error", lambda: f"""def {fn}({v1}):
return {v1} * 2

print({fn}({n1}))
"""),
            ("indentation_error", lambda: f"""def {fn}({v1}, {v2}):
    for i in range({v1}):
    print(i)
"""),
            ("indentation_error", lambda: f"""def check({v1}):
    if {v1} > 0:
        print("positive")
   return True

check({n1})
"""),

            # ── incomplete_statement (3 variants) ─────────────────────────
            ("incomplete_statement", lambda: f"""def {fn}({v1}):
    {v2} =
    return {v2}

print({fn}({n1}))
"""),
            ("incomplete_statement", lambda: f"""def compute({v1}, {v2}):
    return

print(compute({n1}, {n2}))
"""),
            ("incomplete_statement", lambda: f"""{v1} = {n1}
{v2} =
print({v1})
"""),

            # ── invalid_syntax (3 variants) ───────────────────────────────
            ("invalid_syntax", lambda: f"""def {fn}({v1}, {v2}):
    return {v1} ++ {v2}

print({fn}({n1}, {n2}))
"""),
            ("invalid_syntax", lambda: f"""def compute({v1}):
    {v2} = {v1} @@ {n1}
    return {v2}

print(compute({n2}))
"""),
            ("invalid_syntax", lambda: f"""def test():
    {v1} = {n1}
    if {v1} === {n2}:
        print("equal")

test()
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
