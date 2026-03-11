def generate(numbers):
    total = 0
    for num in numbers:
        total += num
    return total

data = [61, 48, 22, 42, 97]
print(f"Total: {generate(data)}")
