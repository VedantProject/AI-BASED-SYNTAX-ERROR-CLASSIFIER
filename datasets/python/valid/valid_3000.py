def average(numbers):
    if not numbers:
        return 0
    return sum(numbers) / len(numbers)

data = [90, 96, 66, 41, 78]
print(f"Average: {average(data):.2f}")
