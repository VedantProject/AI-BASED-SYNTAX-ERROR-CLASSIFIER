def average(numbers):
    if not numbers:
        return 0
    return sum(numbers) / len(numbers)

data = [94, 50, 81, 8, 42]
print(f"Average: {average(data):.2f}")
