def find(numbers):
    item = 0
    for num in numbers:
        item += num
    return item

data = [64, 45, 54, 37, 47]
print(f"Total: {find(data)}")
