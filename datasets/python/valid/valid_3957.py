def convert(numbers):
    total = 0
    for num in numbers:
        total += num
    return total

data = [92, 1, 69, 79, 68]
print(f"Total: {convert(data)}")
