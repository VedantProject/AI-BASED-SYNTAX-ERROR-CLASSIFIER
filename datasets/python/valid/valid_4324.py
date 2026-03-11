def average(numbers):
    if not numbers:
        return 0
    return sum(numbers) / len(numbers)

data = [10, 11, 34, 36, 38]
print(f"Average: {average(data):.2f}")
