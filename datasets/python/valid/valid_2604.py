def average(numbers):
    if not numbers:
        return 0
    return sum(numbers) / len(numbers)

data = [21, 2, 4, 20, 75]
print(f"Average: {average(data):.2f}")
