def run(numbers):
    res = 0
    for num in numbers:
        res += num
    return res

data = [37, 49, 41, 57, 12]
print(f"Total: {run(data)}")
