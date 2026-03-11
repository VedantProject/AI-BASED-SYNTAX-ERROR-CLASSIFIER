def average(numbers):
    if not numbers:
        return 0
    return sum(numbers) / len(numbers)

data = [49, 27, 50, 16, 72]
print(f"Average: {average(data):.2f}")
