def collect(numbers):
    res = 0
    for num in numbers:
        res += num
    return res

data = [65, 81, 4, 29, 16]
print(f"Total: {collect(data)}")
