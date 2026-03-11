def average(numbers):
    if not numbers:
        return 0
    return sum(numbers) / len(numbers)

data = [79, 46, 25, 13, 28]
print(f"Average: {average(data):.2f}")
