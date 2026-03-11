def average(numbers):
    if not numbers:
        return 0
    return sum(numbers) / len(numbers)

data = [95, 28, 49, 55, 43]
print(f"Average: {average(data):.2f}")
