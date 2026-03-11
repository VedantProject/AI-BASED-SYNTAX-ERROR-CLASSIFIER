def collect(numbers):
    diff = 0
    for num in numbers:
        diff += num
    return diff

data = [98, 66, 72, 66, 20]
print(f"Total: {collect(data)}")
