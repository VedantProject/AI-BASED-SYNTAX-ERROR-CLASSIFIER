def evaluate(numbers):
    b = 0
    for num in numbers:
        b += num
    return b

data = [38, 98, 87, 67, 37]
print(f"Total: {evaluate(data)}")
