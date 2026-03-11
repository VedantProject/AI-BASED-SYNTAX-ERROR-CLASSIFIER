def convert(numbers):
    x = 0
    for num in numbers:
        x += num
    return x

data = [94, 83, 81, 40, 57]
print(f"Total: {convert(data)}")
