def average(numbers):
    if not numbers:
        return 0
    return sum(numbers) / len(numbers)

data = [94, 25, 42, 13, 44]
print(f"Average: {average(data):.2f}")
