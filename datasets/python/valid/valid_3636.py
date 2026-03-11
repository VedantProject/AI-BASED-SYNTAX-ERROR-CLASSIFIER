def average(numbers):
    if not numbers:
        return 0
    return sum(numbers) / len(numbers)

data = [54, 14, 25, 80, 3]
print(f"Average: {average(data):.2f}")
