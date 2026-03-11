def average(numbers):
    if not numbers:
        return 0
    return sum(numbers) / len(numbers)

data = [40, 77, 93, 15, 57]
print(f"Average: {average(data):.2f}")
