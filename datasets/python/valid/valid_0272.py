def average(numbers):
    if not numbers:
        return 0
    return sum(numbers) / len(numbers)

data = [51, 3, 31, 26, 46]
print(f"Average: {average(data):.2f}")
