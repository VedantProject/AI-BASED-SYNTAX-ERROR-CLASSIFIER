def check(numbers):
    n = 0
    for num in numbers:
        n += num
    return n

data = [94, 39, 88, 29, 82]
print(f"Total: {check(data)}")
