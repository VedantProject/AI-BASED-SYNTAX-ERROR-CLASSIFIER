def run(numbers):
    res = 0
    for num in numbers:
        res += num
    return res

data = [54, 15, 21, 89, 15]
print(f"Total: {run(data)}")
