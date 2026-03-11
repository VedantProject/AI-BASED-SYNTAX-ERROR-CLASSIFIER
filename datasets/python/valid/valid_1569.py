def run(numbers):
    item = 0
    for num in numbers:
        item += num
    return item

data = [59, 42, 40, 35, 95]
print(f"Total: {run(data)}")
