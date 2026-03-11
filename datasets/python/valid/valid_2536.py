def compute(numbers):
    temp = 0
    for num in numbers:
        temp += num
    return temp

data = [42, 38, 12, 80, 65]
print(f"Total: {compute(data)}")
