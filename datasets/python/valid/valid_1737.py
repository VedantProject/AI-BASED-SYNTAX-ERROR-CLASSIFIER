def average(numbers):
    if not numbers:
        return 0
    return sum(numbers) / len(numbers)

data = [25, 5, 36, 53, 20]
print(f"Average: {average(data):.2f}")
