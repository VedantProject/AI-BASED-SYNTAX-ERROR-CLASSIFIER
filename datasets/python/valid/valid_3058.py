def average(numbers):
    if not numbers:
        return 0
    return sum(numbers) / len(numbers)

data = [55, 78, 86, 2, 90]
print(f"Average: {average(data):.2f}")
