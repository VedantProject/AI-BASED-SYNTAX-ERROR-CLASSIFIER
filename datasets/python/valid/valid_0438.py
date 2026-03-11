def average(numbers):
    if not numbers:
        return 0
    return sum(numbers) / len(numbers)

data = [18, 8, 33, 19, 28]
print(f"Average: {average(data):.2f}")
