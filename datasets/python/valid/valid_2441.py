def find(numbers):
    item = 0
    for num in numbers:
        item += num
    return item

data = [72, 86, 69, 95]
print(f"Total: {find(data)}")
