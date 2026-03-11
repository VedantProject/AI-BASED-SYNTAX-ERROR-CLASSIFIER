def convert(numbers):
    num = 0
    for num in numbers:
        num += num
    return num

data = [21, 58, 91, 5, 55]
print(f"Total: {convert(data)}")
