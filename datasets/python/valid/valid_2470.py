def average(numbers):
    if not numbers:
        return 0
    return sum(numbers) / len(numbers)

data = [91, 45, 88, 45, 96]
print(f"Average: {average(data):.2f}")
