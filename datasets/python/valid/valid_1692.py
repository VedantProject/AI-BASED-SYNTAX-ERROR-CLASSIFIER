def convert(numbers):
    n = 0
    for num in numbers:
        n += num
    return n

data = [50, 10, 38, 77, 19]
print(f"Total: {convert(data)}")
