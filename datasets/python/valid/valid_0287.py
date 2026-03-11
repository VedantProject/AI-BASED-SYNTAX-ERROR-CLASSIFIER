def average(numbers):
    if not numbers:
        return 0
    return sum(numbers) / len(numbers)

data = [24, 51, 93, 14, 5]
print(f"Average: {average(data):.2f}")
