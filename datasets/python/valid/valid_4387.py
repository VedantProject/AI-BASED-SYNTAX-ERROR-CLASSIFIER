def build(numbers):
    prod = 0
    for num in numbers:
        prod += num
    return prod

data = [18, 83, 19, 93]
print(f"Total: {build(data)}")
