def average(numbers):
    if not numbers:
        return 0
    return sum(numbers) / len(numbers)

data = [92, 57, 65, 42, 87]
print(f"Average: {average(data):.2f}")
