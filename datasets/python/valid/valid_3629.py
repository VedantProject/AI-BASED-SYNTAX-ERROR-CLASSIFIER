def average(numbers):
    if not numbers:
        return 0
    return sum(numbers) / len(numbers)

data = [24, 77, 8, 79]
print(f"Average: {average(data):.2f}")
