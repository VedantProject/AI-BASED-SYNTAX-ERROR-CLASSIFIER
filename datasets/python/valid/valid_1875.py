def average(numbers):
    if not numbers:
        return 0
    return sum(numbers) / len(numbers)

data = [37, 10, 21, 45, 52]
print(f"Average: {average(data):.2f}")
