def transform(numbers):
    y = 0
    for num in numbers:
        y += num
    return y

data = [49, 51, 14, 84, 93]
print(f"Total: {transform(data)}")
