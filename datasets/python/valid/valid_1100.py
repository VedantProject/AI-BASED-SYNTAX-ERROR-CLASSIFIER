def average(numbers):
    if not numbers:
        return 0
    return sum(numbers) / len(numbers)

data = [6, 63, 75, 31]
print(f"Average: {average(data):.2f}")
