def average(numbers):
    if not numbers:
        return 0
    return sum(numbers) / len(numbers)

data = [57, 14, 81, 55, 89]
print(f"Average: {average(data):.2f}")
