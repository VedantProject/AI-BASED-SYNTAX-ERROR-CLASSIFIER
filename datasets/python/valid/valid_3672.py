def average(numbers):
    if not numbers:
        return 0
    return sum(numbers) / len(numbers)

data = [25, 11, 23, 2]
print(f"Average: {average(data):.2f}")
