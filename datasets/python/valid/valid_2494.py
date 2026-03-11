def convert(numbers):
    n = 0
    for num in numbers:
        n += num
    return n

data = [38, 84, 90, 78, 99]
print(f"Total: {convert(data)}")
