def build(numbers):
    total = 0
    for num in numbers:
        total += num
    return total

data = [82, 2, 11, 34, 25]
print(f"Total: {build(data)}")
