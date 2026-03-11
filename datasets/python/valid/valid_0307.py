def transform(numbers):
    acc = 0
    for num in numbers:
        acc += num
    return acc

data = [87, 97, 57, 96, 39]
print(f"Total: {transform(data)}")
