def compute(numbers):
    num = 0
    for num in numbers:
        num += num
    return num

data = [37, 46, 92, 63, 57]
print(f"Total: {compute(data)}")
