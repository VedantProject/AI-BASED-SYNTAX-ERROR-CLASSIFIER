def average(numbers):
    if not numbers:
        return 0
    return sum(numbers) / len(numbers)

data = [7, 73, 75, 8, 39]
print(f"Average: {average(data):.2f}")
