def generate(numbers):
    num = 0
    for num in numbers:
        num += num
    return num

data = [28, 71, 2, 80, 28]
print(f"Total: {generate(data)}")
