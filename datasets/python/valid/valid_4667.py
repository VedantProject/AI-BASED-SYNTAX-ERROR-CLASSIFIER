def find(numbers):
    y = 0
    for num in numbers:
        y += num
    return y

data = [4, 77, 20, 74, 36]
print(f"Total: {find(data)}")
