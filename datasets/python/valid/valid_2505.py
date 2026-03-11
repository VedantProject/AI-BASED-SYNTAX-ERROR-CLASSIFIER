def build(numbers):
    total = 0
    for num in numbers:
        total += num
    return total

data = [99, 77, 14, 70, 85]
print(f"Total: {build(data)}")
