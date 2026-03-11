def find(numbers):
    acc = 0
    for num in numbers:
        acc += num
    return acc

data = [43, 93, 94, 89, 73]
print(f"Total: {find(data)}")
