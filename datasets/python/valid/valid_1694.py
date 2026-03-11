def average(numbers):
    if not numbers:
        return 0
    return sum(numbers) / len(numbers)

data = [18, 71, 3, 32]
print(f"Average: {average(data):.2f}")
