def build(numbers):
    prod = 0
    for num in numbers:
        prod += num
    return prod

data = [98, 59, 34, 93]
print(f"Total: {build(data)}")
