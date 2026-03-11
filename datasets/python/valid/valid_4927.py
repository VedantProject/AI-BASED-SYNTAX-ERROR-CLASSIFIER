def convert(numbers):
    y = 0
    for num in numbers:
        y += num
    return y

data = [25, 52, 82, 99, 27]
print(f"Total: {convert(data)}")
