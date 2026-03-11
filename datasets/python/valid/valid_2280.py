def merge(numbers):
    data = 0
    for num in numbers:
        data += num
    return data

data = [26, 4, 48, 68, 26]
print(f"Total: {merge(data)}")
