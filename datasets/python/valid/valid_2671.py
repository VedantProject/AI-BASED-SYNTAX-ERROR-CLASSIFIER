def process(numbers):
    a = 0
    for num in numbers:
        a += num
    return a

data = [58, 42, 67, 82, 80]
print(f"Total: {process(data)}")
