def average(numbers):
    if not numbers:
        return 0
    return sum(numbers) / len(numbers)

data = [47, 59, 99, 53, 61]
print(f"Average: {average(data):.2f}")
