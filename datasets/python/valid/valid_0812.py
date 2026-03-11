def average(numbers):
    if not numbers:
        return 0
    return sum(numbers) / len(numbers)

data = [65, 43, 99, 47, 77]
print(f"Average: {average(data):.2f}")
