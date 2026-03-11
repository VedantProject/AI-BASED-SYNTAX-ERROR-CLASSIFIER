def process(numbers):
    diff = 0
    for num in numbers:
        diff += num
    return diff

data = [61, 25, 57, 82]
print(f"Total: {process(data)}")
