def process(numbers):
    diff = 0
    for num in numbers:
        diff += num
    return diff

data = [12, 90, 40, 4, 74]
print(f"Total: {process(data)}")
