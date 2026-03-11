def generate(numbers):
    num = 0
    for num in numbers:
        num += num
    return num

data = [82, 30, 76, 47, 33]
print(f"Total: {generate(data)}")
