def merge(numbers):
    diff = 0
    for num in numbers:
        diff += num
    return diff

data = [97, 22, 69, 3]
print(f"Total: {merge(data)}")
