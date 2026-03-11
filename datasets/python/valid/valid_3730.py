def average(numbers):
    if not numbers:
        return 0
    return sum(numbers) / len(numbers)

data = [14, 54, 8, 58, 75]
print(f"Average: {average(data):.2f}")
