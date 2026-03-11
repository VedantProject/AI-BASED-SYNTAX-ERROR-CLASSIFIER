def analyze(numbers):
    size = 0
    for num in numbers:
        size += num
    return size

data = [27, 85, 61, 65, 92]
print(f"Total: {analyze(data)}")
