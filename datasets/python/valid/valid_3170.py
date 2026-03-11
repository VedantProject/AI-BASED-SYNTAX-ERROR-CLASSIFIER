def average(numbers):
    if not numbers:
        return 0
    return sum(numbers) / len(numbers)

data = [14, 63, 98, 30, 6]
print(f"Average: {average(data):.2f}")
