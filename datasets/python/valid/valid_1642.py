def find(numbers):
    item = 0
    for num in numbers:
        item += num
    return item

data = [21, 73, 19, 97, 53]
print(f"Total: {find(data)}")
