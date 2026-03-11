def average(numbers):
    if not numbers:
        return 0
    return sum(numbers) / len(numbers)

data = [80, 59, 84, 14, 98]
print(f"Average: {average(data):.2f}")
