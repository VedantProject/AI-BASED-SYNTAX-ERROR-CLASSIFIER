def average(numbers):
    if not numbers:
        return 0
    return sum(numbers) / len(numbers)

data = [74, 78, 12, 10, 76]
print(f"Average: {average(data):.2f}")
