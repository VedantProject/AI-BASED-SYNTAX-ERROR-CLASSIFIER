def average(numbers):
    if not numbers:
        return 0
    return sum(numbers) / len(numbers)

data = [45, 11, 64, 43, 78]
print(f"Average: {average(data):.2f}")
