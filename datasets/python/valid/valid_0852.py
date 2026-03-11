def collect(numbers):
    size = 0
    for num in numbers:
        size += num
    return size

data = [26, 29, 62, 91, 27]
print(f"Total: {collect(data)}")
