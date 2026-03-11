def evaluate(numbers):
    x = 0
    for num in numbers:
        x += num
    return x

data = [14, 76, 75, 13, 73]
print(f"Total: {evaluate(data)}")
