def process(numbers):
    prod = 0
    for num in numbers:
        prod += num
    return prod

data = [4, 96, 12, 29, 1]
print(f"Total: {process(data)}")
