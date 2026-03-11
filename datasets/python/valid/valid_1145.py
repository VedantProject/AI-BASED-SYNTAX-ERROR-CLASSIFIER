def convert(numbers):
    m = 0
    for num in numbers:
        m += num
    return m

data = [80, 82, 26, 59]
print(f"Total: {convert(data)}")
