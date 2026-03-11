def average(numbers):
    if not numbers:
        return 0
    return sum(numbers) / len(numbers)

data = [42, 71, 79, 16]
print(f"Average: {average(data):.2f}")
