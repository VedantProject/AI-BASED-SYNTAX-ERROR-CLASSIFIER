def find(numbers):
    total = 0
    for num in numbers:
        total += num
    return total

data = [14, 29, 60, 68, 3]
print(f"Total: {find(data)}")
