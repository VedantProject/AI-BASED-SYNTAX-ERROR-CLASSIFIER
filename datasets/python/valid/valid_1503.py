def average(numbers):
    if not numbers:
        return 0
    return sum(numbers) / len(numbers)

data = [82, 82, 14, 34, 85]
print(f"Average: {average(data):.2f}")
