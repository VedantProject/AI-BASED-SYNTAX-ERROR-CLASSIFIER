def find(numbers):
    a = 0
    for num in numbers:
        a += num
    return a

data = [28, 97, 90, 51, 14]
print(f"Total: {find(data)}")
