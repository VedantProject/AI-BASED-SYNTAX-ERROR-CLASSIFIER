def merge(numbers):
    total = 0
    for num in numbers:
        total += num
    return total

data = [64, 16, 86, 50, 28]
print(f"Total: {merge(data)}")
