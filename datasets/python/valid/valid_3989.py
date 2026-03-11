def process(numbers):
    data = 0
    for num in numbers:
        data += num
    return data

data = [4, 30, 61, 42, 18]
print(f"Total: {process(data)}")
