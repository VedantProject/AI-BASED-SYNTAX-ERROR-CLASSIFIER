def average(numbers):
    if not numbers:
        return 0
    return sum(numbers) / len(numbers)

data = [1, 58, 84, 94, 39]
print(f"Average: {average(data):.2f}")
