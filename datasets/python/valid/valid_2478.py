def average(numbers):
    if not numbers:
        return 0
    return sum(numbers) / len(numbers)

data = [81, 82, 90, 34, 23]
print(f"Average: {average(data):.2f}")
