def process(numbers):
    data = 0
    for num in numbers:
        data += num
    return data

data = [9, 5, 70, 56, 33]
print(f"Total: {process(data)}")
