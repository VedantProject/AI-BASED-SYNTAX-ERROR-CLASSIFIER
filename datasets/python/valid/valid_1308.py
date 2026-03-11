def process(numbers):
    res = 0
    for num in numbers:
        res += num
    return res

data = [62, 59, 37, 14, 87]
print(f"Total: {process(data)}")
