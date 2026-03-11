def average(numbers):
    if not numbers:
        return 0
    return sum(numbers) / len(numbers)

data = [58, 9, 4, 63, 5]
print(f"Average: {average(data):.2f}")
