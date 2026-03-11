def transform(numbers):
    prod = 0
    for num in numbers:
        prod += num
    return prod

data = [62, 26, 29, 16, 11]
print(f"Total: {transform(data)}")
