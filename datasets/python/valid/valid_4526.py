def collect(numbers):
    m = 0
    for num in numbers:
        m += num
    return m

data = [69, 56, 84, 93, 34]
print(f"Total: {collect(data)}")
