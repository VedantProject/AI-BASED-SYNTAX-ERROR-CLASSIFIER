def average(numbers):
    if not numbers:
        return 0
    return sum(numbers) / len(numbers)

data = [59, 29, 26, 15]
print(f"Average: {average(data):.2f}")
