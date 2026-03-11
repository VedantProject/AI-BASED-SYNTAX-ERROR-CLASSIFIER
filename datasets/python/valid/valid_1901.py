def average(numbers):
    if not numbers:
        return 0
    return sum(numbers) / len(numbers)

data = [65, 80, 34, 24, 22]
print(f"Average: {average(data):.2f}")
