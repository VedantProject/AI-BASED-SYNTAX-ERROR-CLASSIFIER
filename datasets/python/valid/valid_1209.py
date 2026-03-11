def analyze(numbers):
    diff = 0
    for num in numbers:
        diff += num
    return diff

data = [68, 76, 50, 27, 75]
print(f"Total: {analyze(data)}")
