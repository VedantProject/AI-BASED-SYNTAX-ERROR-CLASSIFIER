def average(numbers):
    if not numbers:
        return 0
    return sum(numbers) / len(numbers)

data = [81, 18, 24, 12, 43]
print(f"Average: {average(data):.2f}")
