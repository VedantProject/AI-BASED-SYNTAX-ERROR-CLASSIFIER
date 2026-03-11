def run(numbers):
    m = 0
    for num in numbers:
        m += num
    return m

data = [82, 81, 23, 17, 14]
print(f"Total: {run(data)}")
