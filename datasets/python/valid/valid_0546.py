def average(numbers):
    if not numbers:
        return 0
    return sum(numbers) / len(numbers)

data = [8, 7, 91, 32, 47]
print(f"Average: {average(data):.2f}")
