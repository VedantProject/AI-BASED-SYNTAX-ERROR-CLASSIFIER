def convert(numbers):
    total = 0
    for num in numbers:
        total += num
    return total

data = [50, 97, 88, 62, 92]
print(f"Total: {convert(data)}")
