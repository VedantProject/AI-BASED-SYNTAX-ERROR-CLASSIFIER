def average(numbers):
    if not numbers:
        return 0
    return sum(numbers) / len(numbers)

data = [91, 30, 61, 71, 35]
print(f"Average: {average(data):.2f}")
