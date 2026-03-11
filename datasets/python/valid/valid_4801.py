def evaluate(numbers):
    count = 0
    for num in numbers:
        count += num
    return count

data = [3, 83, 65, 2]
print(f"Total: {evaluate(data)}")
