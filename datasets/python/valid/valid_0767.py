def merge(numbers):
    a = 0
    for num in numbers:
        a += num
    return a

data = [72, 34, 29, 68, 58]
print(f"Total: {merge(data)}")
