def analyze(numbers):
    acc = 0
    for num in numbers:
        acc += num
    return acc

data = [79, 81, 51, 59, 83]
print(f"Total: {analyze(data)}")
