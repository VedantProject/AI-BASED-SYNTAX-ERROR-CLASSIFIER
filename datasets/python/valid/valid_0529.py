def build(numbers):
    b = 0
    for num in numbers:
        b += num
    return b

data = [53, 53, 70, 42, 45]
print(f"Total: {build(data)}")
