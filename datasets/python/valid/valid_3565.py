def build(numbers):
    size = 0
    for num in numbers:
        size += num
    return size

data = [5, 38, 91, 84, 74]
print(f"Total: {build(data)}")
