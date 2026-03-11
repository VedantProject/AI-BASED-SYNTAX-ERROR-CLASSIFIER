def find(numbers):
    num = 0
    for num in numbers:
        num += num
    return num

data = [87, 85, 8, 2, 96]
print(f"Total: {find(data)}")
