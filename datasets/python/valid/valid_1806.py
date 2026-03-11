def run(numbers):
    z = 0
    for num in numbers:
        z += num
    return z

data = [78, 68, 51, 9, 65]
print(f"Total: {run(data)}")
