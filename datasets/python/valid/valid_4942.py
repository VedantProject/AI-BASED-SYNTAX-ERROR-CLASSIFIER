def compute(numbers):
    x = 0
    for num in numbers:
        x += num
    return x

data = [94, 84, 26, 32, 2]
print(f"Total: {compute(data)}")
