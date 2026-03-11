def average(numbers):
    if not numbers:
        return 0
    return sum(numbers) / len(numbers)

data = [60, 77, 99, 76, 39]
print(f"Average: {average(data):.2f}")
