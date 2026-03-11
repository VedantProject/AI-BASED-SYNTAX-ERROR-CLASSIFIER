def process(numbers):
    val = 0
    for num in numbers:
        val += num
    return val

data = [45, 21, 53, 68, 77]
print(f"Total: {process(data)}")
