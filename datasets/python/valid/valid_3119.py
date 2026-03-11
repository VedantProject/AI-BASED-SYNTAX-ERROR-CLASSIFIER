def convert(numbers):
    a = 0
    for num in numbers:
        a += num
    return a

data = [77, 57, 13, 56, 74]
print(f"Total: {convert(data)}")
