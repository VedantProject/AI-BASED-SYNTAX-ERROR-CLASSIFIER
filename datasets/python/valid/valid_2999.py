def average(numbers):
    if not numbers:
        return 0
    return sum(numbers) / len(numbers)

data = [16, 93, 6, 40, 98]
print(f"Average: {average(data):.2f}")
