def average(numbers):
    if not numbers:
        return 0
    return sum(numbers) / len(numbers)

data = [74, 94, 90, 87, 98]
print(f"Average: {average(data):.2f}")
