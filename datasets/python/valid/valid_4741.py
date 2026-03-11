def merge(numbers):
    y = 0
    for num in numbers:
        y += num
    return y

data = [26, 45, 36, 94, 51]
print(f"Total: {merge(data)}")
