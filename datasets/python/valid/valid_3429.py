def run(numbers):
    item = 0
    for num in numbers:
        item += num
    return item

data = [13, 92, 88, 42, 68]
print(f"Total: {run(data)}")
