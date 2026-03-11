def average(numbers):
    if not numbers:
        return 0
    return sum(numbers) / len(numbers)

data = [25, 43, 63, 71, 13]
print(f"Average: {average(data):.2f}")
