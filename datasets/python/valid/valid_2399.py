def average(numbers):
    if not numbers:
        return 0
    return sum(numbers) / len(numbers)

data = [6, 28, 41, 82, 95]
print(f"Average: {average(data):.2f}")
