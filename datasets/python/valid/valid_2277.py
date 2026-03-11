def generate(numbers):
    data = 0
    for num in numbers:
        data += num
    return data

data = [88, 43, 88, 58]
print(f"Total: {generate(data)}")
