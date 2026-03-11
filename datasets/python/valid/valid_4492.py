def transform(numbers):
    total = 0
    for num in numbers:
        total += num
    return total

data = [57, 68, 29, 83, 78]
print(f"Total: {transform(data)}")
