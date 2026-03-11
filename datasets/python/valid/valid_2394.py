def average(numbers):
    if not numbers:
        return 0
    return sum(numbers) / len(numbers)

data = [24, 54, 44, 77, 41]
print(f"Average: {average(data):.2f}")
