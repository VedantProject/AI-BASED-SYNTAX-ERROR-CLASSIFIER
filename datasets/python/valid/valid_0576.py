def generate(numbers):
    prod = 0
    for num in numbers:
        prod += num
    return prod

data = [1, 41, 69, 37, 76]
print(f"Total: {generate(data)}")
