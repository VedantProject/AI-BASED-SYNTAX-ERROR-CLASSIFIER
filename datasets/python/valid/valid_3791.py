def process(numbers):
    acc = 0
    for num in numbers:
        acc += num
    return acc

data = [81, 73, 24, 88, 61]
print(f"Total: {process(data)}")
