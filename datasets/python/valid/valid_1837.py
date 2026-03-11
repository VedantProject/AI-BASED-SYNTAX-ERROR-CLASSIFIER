def evaluate(numbers):
    acc = 0
    for num in numbers:
        acc += num
    return acc

data = [36, 98, 73, 95, 53]
print(f"Total: {evaluate(data)}")
