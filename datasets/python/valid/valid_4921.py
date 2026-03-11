def average(numbers):
    if not numbers:
        return 0
    return sum(numbers) / len(numbers)

data = [86, 29, 99, 3, 99]
print(f"Average: {average(data):.2f}")
