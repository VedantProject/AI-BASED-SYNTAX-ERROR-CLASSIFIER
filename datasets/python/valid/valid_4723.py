def compute(numbers):
    acc = 0
    for num in numbers:
        acc += num
    return acc

data = [86, 75, 51, 37]
print(f"Total: {compute(data)}")
