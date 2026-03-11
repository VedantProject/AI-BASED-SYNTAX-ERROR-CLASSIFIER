def convert(numbers):
    y = 0
    for num in numbers:
        y += num
    return y

data = [98, 69, 12, 23, 93]
print(f"Total: {convert(data)}")
