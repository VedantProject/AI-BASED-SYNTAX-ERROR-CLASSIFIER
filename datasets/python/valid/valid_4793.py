def analyze(numbers):
    a = 0
    for num in numbers:
        a += num
    return a

data = [23, 67, 69, 28, 94]
print(f"Total: {analyze(data)}")
