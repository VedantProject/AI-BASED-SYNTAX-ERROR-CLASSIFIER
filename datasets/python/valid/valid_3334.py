def process(numbers):
    b = 0
    for num in numbers:
        b += num
    return b

data = [4, 79, 70, 82, 47]
print(f"Total: {process(data)}")
