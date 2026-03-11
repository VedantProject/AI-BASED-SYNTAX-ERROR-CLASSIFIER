def convert(numbers):
    z = 0
    for num in numbers:
        z += num
    return z

data = [55, 37, 93, 43]
print(f"Total: {convert(data)}")
