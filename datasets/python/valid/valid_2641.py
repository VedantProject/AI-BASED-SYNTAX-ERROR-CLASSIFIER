def average(numbers):
    if not numbers:
        return 0
    return sum(numbers) / len(numbers)

data = [86, 27, 55, 63, 24]
print(f"Average: {average(data):.2f}")
