def generate(numbers):
    size = 0
    for num in numbers:
        size += num
    return size

data = [17, 81, 47, 20, 59]
print(f"Total: {generate(data)}")
