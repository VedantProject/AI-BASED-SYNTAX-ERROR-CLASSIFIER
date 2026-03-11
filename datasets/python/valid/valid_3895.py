def process(numbers):
    diff = 0
    for num in numbers:
        diff += num
    return diff

data = [51, 57, 23, 92, 60]
print(f"Total: {process(data)}")
