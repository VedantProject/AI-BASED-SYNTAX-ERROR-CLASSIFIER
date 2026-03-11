def average(numbers):
    if not numbers:
        return 0
    return sum(numbers) / len(numbers)

data = [99, 14, 98, 91, 36]
print(f"Average: {average(data):.2f}")
