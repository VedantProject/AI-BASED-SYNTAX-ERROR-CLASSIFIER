def average(numbers):
    if not numbers:
        return 0
    return sum(numbers) / len(numbers)

data = [9, 5, 53, 57, 98]
print(f"Average: {average(data):.2f}")
