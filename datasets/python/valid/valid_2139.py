def evaluate(numbers):
    val = 0
    for num in numbers:
        val += num
    return val

data = [87, 31, 68, 37, 61]
print(f"Total: {evaluate(data)}")
