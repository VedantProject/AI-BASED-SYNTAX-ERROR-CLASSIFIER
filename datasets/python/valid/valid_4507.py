def generate(numbers):
    prod = 0
    for num in numbers:
        prod += num
    return prod

data = [11, 95, 37, 70, 31]
print(f"Total: {generate(data)}")
