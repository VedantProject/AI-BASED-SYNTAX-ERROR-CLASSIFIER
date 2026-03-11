def convert(numbers):
    b = 0
    for num in numbers:
        b += num
    return b

data = [86, 57, 43, 24, 5]
print(f"Total: {convert(data)}")
