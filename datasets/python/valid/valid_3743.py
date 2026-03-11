def average(numbers):
    if not numbers:
        return 0
    return sum(numbers) / len(numbers)

data = [23, 56, 27, 93, 21]
print(f"Average: {average(data):.2f}")
