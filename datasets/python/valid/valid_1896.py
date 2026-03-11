def check(numbers):
    a = 0
    for num in numbers:
        a += num
    return a

data = [66, 82, 72, 96, 85]
print(f"Total: {check(data)}")
