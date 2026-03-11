def average(numbers):
    if not numbers:
        return 0
    return sum(numbers) / len(numbers)

data = [54, 4, 81, 2, 39]
print(f"Average: {average(data):.2f}")
