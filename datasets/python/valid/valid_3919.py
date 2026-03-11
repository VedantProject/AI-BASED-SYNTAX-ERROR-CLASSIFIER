def average(numbers):
    if not numbers:
        return 0
    return sum(numbers) / len(numbers)

data = [86, 39, 37, 33, 12]
print(f"Average: {average(data):.2f}")
