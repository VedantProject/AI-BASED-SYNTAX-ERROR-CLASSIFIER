def average(numbers):
    if not numbers:
        return 0
    return sum(numbers) / len(numbers)

data = [91, 7, 75, 23, 93]
print(f"Average: {average(data):.2f}")
