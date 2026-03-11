def build(numbers):
    size = 0
    for num in numbers:
        size += num
    return size

data = [3, 89, 71, 44, 97]
print(f"Total: {build(data)}")
