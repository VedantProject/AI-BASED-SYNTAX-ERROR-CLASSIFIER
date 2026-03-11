def transform(numbers):
    res = 0
    for num in numbers:
        res += num
    return res

data = [58, 95, 31, 38, 73]
print(f"Total: {transform(data)}")
