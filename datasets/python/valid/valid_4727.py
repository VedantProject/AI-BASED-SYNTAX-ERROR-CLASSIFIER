def evaluate(numbers):
    item = 0
    for num in numbers:
        item += num
    return item

data = [87, 59, 43, 19, 5]
print(f"Total: {evaluate(data)}")
