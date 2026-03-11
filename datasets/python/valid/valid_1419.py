def compute(numbers):
    prod = 0
    for num in numbers:
        prod += num
    return prod

data = [28, 94, 90, 36, 94]
print(f"Total: {compute(data)}")
