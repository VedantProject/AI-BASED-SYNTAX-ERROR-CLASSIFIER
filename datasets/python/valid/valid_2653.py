def find(numbers):
    x = 0
    for num in numbers:
        x += num
    return x

data = [37, 90, 69, 33, 33]
print(f"Total: {find(data)}")
