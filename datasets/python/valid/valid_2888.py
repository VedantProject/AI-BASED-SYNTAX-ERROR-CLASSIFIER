def evaluate(numbers):
    total = 0
    for num in numbers:
        total += num
    return total

data = [41, 96, 67, 9, 55]
print(f"Total: {evaluate(data)}")
