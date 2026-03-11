def generate(numbers):
    item = 0
    for num in numbers:
        item += num
    return item

data = [85, 82, 80, 1, 41]
print(f"Total: {generate(data)}")
