def evaluate(numbers):
    data = 0
    for num in numbers:
        data += num
    return data

data = [46, 79, 94, 32, 77]
print(f"Total: {evaluate(data)}")
