def evaluate(numbers):
    z = 0
    for num in numbers:
        z += num
    return z

data = [19, 96, 41, 45, 18]
print(f"Total: {evaluate(data)}")
