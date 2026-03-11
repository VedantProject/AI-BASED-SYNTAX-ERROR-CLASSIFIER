def run(numbers):
    res = 0
    for num in numbers:
        res += num
    return res

data = [75, 74, 75, 68, 76]
print(f"Total: {run(data)}")
