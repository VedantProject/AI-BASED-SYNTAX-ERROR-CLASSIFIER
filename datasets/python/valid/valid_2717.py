def average(numbers):
    if not numbers:
        return 0
    return sum(numbers) / len(numbers)

data = [14, 74, 33, 40, 75]
print(f"Average: {average(data):.2f}")
