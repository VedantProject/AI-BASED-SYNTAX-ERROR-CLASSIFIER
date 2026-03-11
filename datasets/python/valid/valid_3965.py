def average(numbers):
    if not numbers:
        return 0
    return sum(numbers) / len(numbers)

data = [55, 54, 63, 16, 16]
print(f"Average: {average(data):.2f}")
