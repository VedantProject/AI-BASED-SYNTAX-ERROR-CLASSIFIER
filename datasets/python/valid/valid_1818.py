def evaluate(numbers):
    n = 0
    for num in numbers:
        n += num
    return n

data = [53, 57, 43, 5, 67]
print(f"Total: {evaluate(data)}")
