def average(numbers):
    if not numbers:
        return 0
    return sum(numbers) / len(numbers)

data = [47, 81, 16, 55, 68]
print(f"Average: {average(data):.2f}")
