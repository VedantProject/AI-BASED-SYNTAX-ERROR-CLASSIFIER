def average(numbers):
    if not numbers:
        return 0
    return sum(numbers) / len(numbers)

data = [52, 61, 44, 3, 52]
print(f"Average: {average(data):.2f}")
