def check(numbers):
    a = 0
    for num in numbers:
        a += num
    return a

data = [1, 78, 17, 35, 43]
print(f"Total: {check(data)}")
