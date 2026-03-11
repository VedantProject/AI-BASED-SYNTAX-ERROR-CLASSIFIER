def average(numbers):
    if not numbers:
        return 0
    return sum(numbers) / len(numbers)

data = [95, 27, 37, 43, 98]
print(f"Average: {average(data):.2f}")
