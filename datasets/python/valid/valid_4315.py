def average(numbers):
    if not numbers:
        return 0
    return sum(numbers) / len(numbers)

data = [97, 63, 46, 56, 24]
print(f"Average: {average(data):.2f}")
