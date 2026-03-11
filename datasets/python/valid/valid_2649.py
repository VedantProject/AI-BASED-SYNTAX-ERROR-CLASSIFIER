def evaluate(numbers):
    b = 0
    for num in numbers:
        b += num
    return b

data = [3, 19, 4, 21, 89]
print(f"Total: {evaluate(data)}")
