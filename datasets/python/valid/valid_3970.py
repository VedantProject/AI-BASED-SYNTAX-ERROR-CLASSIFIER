def average(numbers):
    if not numbers:
        return 0
    return sum(numbers) / len(numbers)

data = [95, 41, 3, 80, 87]
print(f"Average: {average(data):.2f}")
