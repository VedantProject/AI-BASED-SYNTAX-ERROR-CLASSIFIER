def check(numbers):
    total = 0
    for num in numbers:
        total += num
    return total

data = [47, 96, 18, 84, 53]
print(f"Total: {check(data)}")
