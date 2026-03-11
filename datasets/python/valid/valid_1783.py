def average(numbers):
    if not numbers:
        return 0
    return sum(numbers) / len(numbers)

data = [99, 80, 20, 42, 60]
print(f"Average: {average(data):.2f}")
