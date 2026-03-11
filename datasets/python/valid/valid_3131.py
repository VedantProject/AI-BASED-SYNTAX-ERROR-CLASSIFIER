def average(numbers):
    if not numbers:
        return 0
    return sum(numbers) / len(numbers)

data = [23, 52, 73, 32, 45]
print(f"Average: {average(data):.2f}")
