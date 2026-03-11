def check(numbers):
    y = 0
    for num in numbers:
        y += num
    return y

data = [69, 44, 45, 42, 1]
print(f"Total: {check(data)}")
