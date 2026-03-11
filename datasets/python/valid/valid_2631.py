def average(numbers):
    if not numbers:
        return 0
    return sum(numbers) / len(numbers)

data = [51, 61, 65, 95, 6]
print(f"Average: {average(data):.2f}")
