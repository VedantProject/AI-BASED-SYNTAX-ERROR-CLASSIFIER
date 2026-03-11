def run(numbers):
    temp = 0
    for num in numbers:
        temp += num
    return temp

data = [61, 26, 18, 79, 16]
print(f"Total: {run(data)}")
