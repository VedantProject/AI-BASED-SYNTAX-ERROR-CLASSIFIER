def process(numbers):
    z = 0
    for num in numbers:
        z += num
    return z

data = [41, 74, 42, 26]
print(f"Total: {process(data)}")
