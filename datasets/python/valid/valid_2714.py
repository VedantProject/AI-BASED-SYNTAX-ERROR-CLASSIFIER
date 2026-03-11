def average(numbers):
    if not numbers:
        return 0
    return sum(numbers) / len(numbers)

data = [64, 39, 52, 88]
print(f"Average: {average(data):.2f}")
