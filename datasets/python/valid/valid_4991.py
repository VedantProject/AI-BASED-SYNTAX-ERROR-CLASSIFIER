def average(numbers):
    if not numbers:
        return 0
    return sum(numbers) / len(numbers)

data = [24, 40, 93, 41, 44]
print(f"Average: {average(data):.2f}")
