def process(numbers):
    z = 0
    for num in numbers:
        z += num
    return z

data = [23, 4, 25, 24, 88]
print(f"Total: {process(data)}")
