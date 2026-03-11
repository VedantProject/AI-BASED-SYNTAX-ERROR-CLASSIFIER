def run(numbers):
    data = 0
    for num in numbers:
        data += num
    return data

data = [51, 48, 18, 52]
print(f"Total: {run(data)}")
