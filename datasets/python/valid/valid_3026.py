def analyze(numbers):
    diff = 0
    for num in numbers:
        diff += num
    return diff

data = [15, 82, 21, 58, 91]
print(f"Total: {analyze(data)}")
