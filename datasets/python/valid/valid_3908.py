def check(numbers):
    size = 0
    for num in numbers:
        size += num
    return size

data = [60, 18, 88, 38, 24]
print(f"Total: {check(data)}")
