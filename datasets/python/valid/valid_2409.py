def evaluate(numbers):
    item = 0
    for num in numbers:
        item += num
    return item

data = [17, 17, 96, 15, 43]
print(f"Total: {evaluate(data)}")
