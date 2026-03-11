def average(numbers):
    if not numbers:
        return 0
    return sum(numbers) / len(numbers)

data = [24, 56, 70, 29, 26]
print(f"Average: {average(data):.2f}")
