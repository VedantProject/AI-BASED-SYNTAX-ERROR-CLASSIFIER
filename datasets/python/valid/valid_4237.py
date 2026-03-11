def average(numbers):
    if not numbers:
        return 0
    return sum(numbers) / len(numbers)

data = [25, 25, 28, 1, 33]
print(f"Average: {average(data):.2f}")
