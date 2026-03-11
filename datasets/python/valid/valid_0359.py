def check(numbers):
    z = 0
    for num in numbers:
        z += num
    return z

data = [82, 90, 8, 92, 59]
print(f"Total: {check(data)}")
