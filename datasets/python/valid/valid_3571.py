def average(numbers):
    if not numbers:
        return 0
    return sum(numbers) / len(numbers)

data = [54, 37, 69, 42, 88]
print(f"Average: {average(data):.2f}")
