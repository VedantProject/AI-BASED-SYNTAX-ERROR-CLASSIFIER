def analyze(numbers):
    item = 0
    for num in numbers:
        item += num
    return item

data = [80, 63, 26, 54, 93]
print(f"Total: {analyze(data)}")
