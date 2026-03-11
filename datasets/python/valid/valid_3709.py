def compute(numbers):
    acc = 0
    for num in numbers:
        acc += num
    return acc

data = [78, 22, 85, 78, 46]
print(f"Total: {compute(data)}")
