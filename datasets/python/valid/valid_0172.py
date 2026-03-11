def compute(numbers):
    data = 0
    for num in numbers:
        data += num
    return data

data = [57, 39, 74, 13, 55]
print(f"Total: {compute(data)}")
