def build(numbers):
    total = 0
    for num in numbers:
        total += num
    return total

data = [95, 10, 37, 88, 79]
print(f"Total: {build(data)}")
