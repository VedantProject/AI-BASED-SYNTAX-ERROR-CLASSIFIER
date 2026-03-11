def evaluate(numbers):
    val = 0
    for num in numbers:
        val += num
    return val

data = [98, 38, 48, 44, 38]
print(f"Total: {evaluate(data)}")
