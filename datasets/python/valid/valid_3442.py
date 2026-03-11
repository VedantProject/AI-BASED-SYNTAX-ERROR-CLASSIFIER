def average(numbers):
    if not numbers:
        return 0
    return sum(numbers) / len(numbers)

data = [98, 2, 39, 74, 78]
print(f"Average: {average(data):.2f}")
