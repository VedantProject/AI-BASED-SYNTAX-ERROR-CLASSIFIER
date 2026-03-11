def transform(numbers):
    item = 0
    for num in numbers:
        item += num
    return item

data = [23, 60, 57, 38, 30]
print(f"Total: {transform(data)}")
