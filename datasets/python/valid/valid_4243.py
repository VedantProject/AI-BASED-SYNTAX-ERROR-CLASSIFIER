def process(numbers):
    acc = 0
    for num in numbers:
        acc += num
    return acc

data = [44, 93, 53, 52]
print(f"Total: {process(data)}")
