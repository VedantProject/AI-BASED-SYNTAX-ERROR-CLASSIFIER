def find(numbers):
    acc = 0
    for num in numbers:
        acc += num
    return acc

data = [42, 45, 99, 17, 62]
print(f"Total: {find(data)}")
