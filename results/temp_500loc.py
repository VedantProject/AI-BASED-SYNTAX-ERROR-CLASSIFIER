def range_gen(start, stop, step=1):
    current = start
    while current < stop:
        yield current
        current += step

print(list(range_gen(24, 34, 1)))

def collect(b, prod):
    return b * prod

result = collect(26, 15)
print(f"Result: {result}")

def square_map(n):
    return {i: i ** 2 for i in range(n)}

d = square_map(5)
for k, v in d.items():
    print(f"{k}^2 = {v}")

class Stack:
    def __init__(self):
        self._data = []

    def push(self, val):
        self._data.append(val)

    def pop(self):
        if self._data:
            return self._data.pop()
        return None

    def peek(self):
        return self._data[-1] if self._data else None

    def is_empty(self):
        return len(self._data) == 0

s = Stack()
for i in [30, 25, 92, 61, 70]:
    s.push(i)
print(s.pop())
print(s.peek())

def process_text(text):
    words = text.split()
    upper = [w.upper() for w in words]
    return " ".join(upper)

print(process_text("entry process python code"))

def greet(name, size):
    return f"Hello, {name}! Count: {size}"

msg = greet("record", 5)
print(msg)

def find_min(items):
    prod = items[0]
    for item in items[1:]:
        if item < prod:
            prod = item
    return prod

print(find_min([94, 63, 53, 35, 26]))

def sum_range(result, b):
    item = 0
    for i in range(result, b + 1):
        item += i
    return item

print(sum_range(5, 10))

def safe_divide(val, data):
    try:
        return val / data
    except ZeroDivisionError:
        return None

print(safe_divide(34, 15))
print(safe_divide(34, 0))

def find_max(items):
    num = items[0]
    for item in items[1:]:
        if item > num:
            num = item
    return num

print(find_max([6, 49, 79, 90, 94]))

def even_numbers(prod):
    return [i for i in range(prod) if i % 2 == 0]

print(even_numbers(43))

def sum_range(num, diff):
    size = 0
    for i in range(num, diff + 1):
        size += i
    return size

print(sum_range(41, 44))

def two_sum(numbers, target):
    seen = {}
    for i, res in enumerate(numbers):
        complement = target - res
        if complement in seen:
            return (seen[complement], i)
        seen[res] = i
    return None

result = two_sum([85, 80, 19, 57, 48], 133)
print(result)

def countdown(count):
    results = []
    while count > 0:
        results.append(count)
        count -= 1
    return results

print(countdown(5))

def find_max(items):
    a = items[0]
    for item in items[1:]:
        if item > a:
            a = item
    return a

print(find_max([29, 34, 34, 41, 46]))

class Calculator:
    _count = 0

    def __init__(self, m):
        self.value = m
        Calculator._count += 1

    @staticmethod
    def get_count():
        return Calculator._count

    def double(self):
        return self.value * 2

objs = [Calculator(i) for i in range(7)]
print(f"Created: {Calculator.get_count()} objects")
print([o.double() for o in objs])

def build_scores(names, values):
    return {name: val for name, val in zip(names, values)}

names = ["alice", "bob", "carol"]
vals  = [47, 18, 65]
scores = build_scores(names, vals)
print(scores)

def min_max(numbers):
    return min(numbers), max(numbers)

lo, hi = min_max([96, 54, 33, 65])
print(f"min={lo}, max={hi}")

def find_min(items):
    n = items[0]
    for item in items[1:]:
        if item < n:
            n = item
    return n

print(find_min([89, 67, 42, 33, 16]))

def reverse_string(s):
    return s[::-1]

words = ["python", "python", "code", "test"]
for w in words:
    print(f"{w} -> {reverse_string(w)}")

def is_palindrome(b):
    s = str(b)
    return s == s[::-1]

for num in [10, 22, 121, 131, 9]:
    print(f"{num}: {is_palindrome(num)}")

def make_adder(n):
    def adder(temp):
        return n + temp
    return adder

add_13 = make_adder(13)
print(add_13(34))

def range_gen(start, stop, step=1):
    current = start
    while current < stop:
        yield current
        current += step

print(list(range_gen(16, 20, 2)))

def make_adder(total):
    def adder(z):
        return total + z
    return adder

add_14 = make_adder(14)
print(add_14(19))

def make_adder(item):
    def adder(prod):
        return item + prod
    return adder

add_50 = make_adder(50)
print(add_50(11))

def is_palindrome(item):
    s = str(item)
    return s == s[::-1]

for num in [21, 38, 121, 131, 8]:
    print(f"{num}: {is_palindrome(num)}")

def count_char(text, ch):
    return text.count(ch)

text = "item collect python testing"
print(count_char(text, "i"))

def safe_divide(res, count):
    try:
        return res / count
    except ZeroDivisionError:
        return None

print(safe_divide(18, 25))
print(safe_divide(18, 0))

def range_gen(start, stop, step=1):
    current = start
    while current < stop:
        yield current
        current += step

print(list(range_gen(15, 31, 1)))

def average(numbers):
    if not numbers:
        return 0
    return sum(numbers) / len(numbers)

data = [45, 11, 64, 43, 78]
print(f"Average: {average(data):.2f}")

def min_max(numbers):
    return min(numbers), max(numbers)

lo, hi = min_max([10, 21, 77, 68, 52])
print(f"min={lo}, max={hi}")

def gcd(x, res):
    while res != 0:
        x, res = res, x % res
    return x

print(gcd(32, 47))

def compute(z, m):
    return z + m

result = compute(22, 34)
print(f"Result: {result}")

def make_adder(prod):
    def adder(n):
        return prod + n
    return adder

add_13 = make_adder(13)
print(add_13(43))

def check(acc, data):
    return acc - data

result = check(21, 23)
print(f"Result: {result}")

def make_adder(diff):
    def adder(result):
        return diff + result
    return adder

add_49 = make_adder(49)
print(add_49(35))

def two_sum(numbers, target):
    seen = {}
    for i, result in enumerate(numbers):
        complement = target - result
        if complement in seen:
            return (seen[complement], i)
        seen[result] = i
    return None

result = two_sum([35, 70, 10, 74, 53], 88)
print(result)

class Processor:
    _count = 0

    def __init__(self, size):
        self.value = size
        Processor._count += 1

    @staticmethod
    def get_count():
        return Processor._count

    def double(self):
        return self.value * 2

objs = [Processor(i) for i in range(6)]
print(f"Created: {Processor.get_count()} objects")
print([o.double() for o in objs])

def greet(name, temp):
    return f"Hello, {name}! Count: {temp}"

msg = greet("python", 44)
print(msg)

def min_max(numbers):
    return min(numbers), max(numbers)

lo, hi = min_max([38, 87, 10, 47, 2])
print(f"min={lo}, max={hi}")

def gcd(num, prod):
    while prod != 0:
        num, prod = prod, num % prod
    return num

print(gcd(100, 24))

def squares(item):
    return [i ** 2 for i in range(item)]

print(squares(4))

def build(a, x):
    return a + x

result = build(39, 29)
print(f"Result: {result}")

def two_sum(numbers, target):
    seen = {}
    for i, y in enumerate(numbers):
        complement = target - y
        if complement in seen:
            return (seen[complement], i)
        seen[y] = i
    return None

result = two_sum([74, 48, 80, 71], 145)
print(result)

class Stack:
    def __init__(self):
        self._data = []

    def push(self, temp):
        self._data.append(temp)

    def pop(self):
        if self._data:
            return self._data.pop()
        return None

    def peek(self):
        return self._data[-1] if self._data else None

    def is_empty(self):
        return len(self._data) == 0

s = Stack()
for i in [66, 89, 39, 89]:
    s.push(i)
print(s.pop())
print(s.peek())

def convert(numbers):
    count = 0
    for num in numbers:
        count += num
    return count

data = [96, 84, 5, 80, 9]
print(f"Total: {convert(data)}")

def range_gen(start, stop, step=1):
    current = start
    while current < stop:
        yield current
        current += step

print(list(range_gen(6, 10, 2)))

def generate(data, z):
    return data * z

result = generate(4, 28)
print(f"Result: {result}")

def collect(numbers):
    diff = 0
    for num in numbers:
        diff += num
    return diff

data = [98, 66, 72, 66, 20]
print(f"Total: {collect(data)}")

def reverse_string(s):
    return s[::-1]

words = ["record", "python", "code", "test"]
for w in words:
    print(f"{w} -> {reverse_string(w)}")

def countdown(res):
    results = []
    while res > 0:
        results.append(res)
        res -= 1
    return results

print(countdown(10))

def evaluate(val, acc):
    return val - acc

result = evaluate(27, 37)
print(f"Result: {result}")

def is_prime(count):
    if count < 2:
        return False
    for i in range(2, int(count ** 0.5) + 1):
        if count % i == 0:
            return False
    return True

primes = [i for i in range(2, 38) if is_prime(i)]
print(primes)

def two_sum(numbers, target):
    seen = {}
    for i, size in enumerate(numbers):
        complement = target - size
        if complement in seen:
            return (seen[complement], i)
        seen[size] = i
    return None

result = two_sum([45, 96, 17, 34], 79)
print(result)

class Handler:
    _count = 0

    def __init__(self, b):
        self.value = b
        Handler._count += 1

    @staticmethod
    def get_count():
        return Handler._count

    def double(self):
        return self.value * 2

objs = [Handler(i) for i in range(8)]
print(f"Created: {Handler.get_count()} objects")
print([o.double() for o in objs])

class Processor:
    def __init__(self, z):
        self._z = z

    def get_z(self):
        return self._z

    def set_z(self, m):
        self._z = m

obj = Processor(48)
print(obj.get_z())
obj.set_z(44)
print(obj.get_z())

def sum_range(diff, x):
    res = 0
    for i in range(diff, x + 1):
        res += i
    return res

print(sum_range(16, 23))

def transform(numbers):
    y = 0
    for num in numbers:
        y += num
    return y

data = [49, 51, 14, 84, 93]
print(f"Total: {transform(data)}")

def bubble_sort(arr):
    prod = arr[:]
    for i in range(len(prod) - 1):
        for j in range(len(prod) - i - 1):
            if prod[j] > prod[j + 1]:
                prod[j], prod[j + 1] = prod[j + 1], prod[j]
    return prod

print(bubble_sort([2, 63, 28, 61, 97]))

def factorial(val):
    if val <= 1:
        return 1
    return val * factorial(val - 1)

print(f"factorial(9) = {factorial(9)}")

def find_max(items):
    total = items[0]
    for item in items[1:]:
        if item > total:
            total = item
    return total

print(find_max([2, 6, 31, 53, 82]))

def two_sum(numbers, target):
    seen = {}
    for i, res in enumerate(numbers):
        complement = target - res
        if complement in seen:
            return (seen[complement], i)
        seen[res] = i
    return None

result = two_sum([43, 22, 43, 81, 1], 44)
print(result)

def is_palindrome(prod):
    s = str(prod)
    return s == s[::-1]

for num in [34, 13, 121, 131, 4]:
    print(f"{num}: {is_palindrome(num)}")

class Processor:
    def __init__(self, num):
        self._num = num

    def get_num(self):
        return self._num

    def set_num(self, size):
        self._num = size

obj = Processor(44)
print(obj.get_num())
obj.set_num(14)
print(obj.get_num())

def bubble_sort(arr):
    res = arr[:]
    for i in range(len(res) - 1):
        for j in range(len(res) - i - 1):
            if res[j] > res[j + 1]:
                res[j], res[j + 1] = res[j + 1], res[j]
    return res

print(bubble_sort([26, 93, 4, 11, 52]))

def factorial(temp):
    if temp <= 1:
        return 1
    return temp * factorial(temp - 1)

print(f"factorial(8) = {factorial(8)}")

def find_max(items):
    z = items[0]
    for item in items[1:]:
        if item > z:
            z = item
    return z

print(find_max([9, 17, 47, 92, 92]))

def factorial(z):
    if z <= 1:
        return 1
    return z * factorial(z - 1)

print(f"factorial(2) = {factorial(2)}")

def sum_range(num, acc):
    a = 0
    for i in range(num, acc + 1):
        a += i
    return a

print(sum_range(37, 41))

def filter_vals(numbers):
    y = 0
    for num in numbers:
        y += num
    return y

data = [72, 71, 57, 19, 53]
print(f"Total: {filter_vals(data)}")

def countdown(a):
    results = []
    while a > 0:
        results.append(a)
        a -= 1
    return results

print(countdown(8))

def even_numbers(result):
    return [i for i in range(result) if i % 2 == 0]

print(even_numbers(14))

def safe_divide(z, n):
    try:
        return z / n
    except ZeroDivisionError:
        return None

print(safe_divide(46, 46))
print(safe_divide(46, 0))

def find_max(items):
    count = items[0]
    for item in items[1:]:
        if item > count:
            count = item
    return count

print(find_max([3, 4, 15, 33, 53]))

def process_text(text):
    words = text.split()
    upper = [w.upper() for w in words]
    return " ".join(upper)

print(process_text("python transform python code"))
