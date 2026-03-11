def build(numbers):
    val = 0
    for num in numbers:
        val += num
    return val

data = [52, 51, 80, 3, 9]
print(f"Total: {build(data)}")
