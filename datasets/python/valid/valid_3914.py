def collect(numbers):
    diff = 0
    for num in numbers:
        diff += num
    return diff

data = [47, 52, 40, 64, 4]
print(f"Total: {collect(data)}")
