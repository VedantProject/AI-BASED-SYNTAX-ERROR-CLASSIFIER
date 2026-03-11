def average(numbers):
    if not numbers:
        return 0
    return sum(numbers) / len(numbers)

data = [99, 75, 19, 61, 75]
print(f"Average: {average(data):.2f}")
