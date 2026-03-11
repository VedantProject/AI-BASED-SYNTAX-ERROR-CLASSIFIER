def collect(numbers):
    z = 0
    for num in numbers:
        z += num
    return z

data = [32, 92, 40, 13, 10]
print(f"Total: {collect(data)}")
