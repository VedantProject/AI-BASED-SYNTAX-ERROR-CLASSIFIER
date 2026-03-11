def merge(numbers):
    res = 0
    for num in numbers:
        res += num
    return res

data = [47, 28, 14, 47, 57]
print(f"Total: {merge(data)}")
