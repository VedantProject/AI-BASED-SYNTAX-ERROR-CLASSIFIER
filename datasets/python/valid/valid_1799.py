def convert(numbers):
    val = 0
    for num in numbers:
        val += num
    return val

data = [17, 37, 87, 32, 31]
print(f"Total: {convert(data)}")
