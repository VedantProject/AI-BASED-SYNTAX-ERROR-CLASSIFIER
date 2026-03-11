def process(numbers):
    diff = 0
    for num in numbers:
        diff += num
    return diff

data = [2, 7, 75, 98, 76]
print(f"Total: {process(data)}")
