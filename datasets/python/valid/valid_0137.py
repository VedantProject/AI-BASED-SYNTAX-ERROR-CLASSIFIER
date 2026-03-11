def find(numbers):
    z = 0
    for num in numbers:
        z += num
    return z

data = [18, 55, 67, 67, 43]
print(f"Total: {find(data)}")
