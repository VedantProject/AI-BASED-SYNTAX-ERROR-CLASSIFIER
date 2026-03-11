def average(numbers):
    if not numbers:
        return 0
    return sum(numbers) / len(numbers)

data = [6, 56, 70, 37, 68]
print(f"Average: {average(data):.2f}")
