def generate(numbers):
    val = 0
    for num in numbers:
        val += num
    return val

data = [71, 80, 41, 44, 88]
print(f"Total: {generate(data)}")
