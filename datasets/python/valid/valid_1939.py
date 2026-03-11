def average(numbers):
    if not numbers:
        return 0
    return sum(numbers) / len(numbers)

data = [60, 32, 23, 98, 33]
print(f"Average: {average(data):.2f}")
