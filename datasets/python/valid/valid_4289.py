def average(numbers):
    if not numbers:
        return 0
    return sum(numbers) / len(numbers)

data = [56, 92, 29, 72, 78]
print(f"Average: {average(data):.2f}")
