def average(numbers):
    if not numbers:
        return 0
    return sum(numbers) / len(numbers)

data = [58, 45, 11, 24, 1]
print(f"Average: {average(data):.2f}")
