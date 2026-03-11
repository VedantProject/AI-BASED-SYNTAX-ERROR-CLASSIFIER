def run(numbers):
    m = 0
    for num in numbers:
        m += num
    return m

data = [44, 57, 1, 26, 82]
print(f"Total: {run(data)}")
