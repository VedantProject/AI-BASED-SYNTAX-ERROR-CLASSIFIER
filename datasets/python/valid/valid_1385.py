def collect(numbers):
    b = 0
    for num in numbers:
        b += num
    return b

data = [62, 37, 22, 21, 32]
print(f"Total: {collect(data)}")
