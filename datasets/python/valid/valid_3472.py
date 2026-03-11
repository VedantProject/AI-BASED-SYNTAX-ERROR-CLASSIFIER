def average(numbers):
    if not numbers:
        return 0
    return sum(numbers) / len(numbers)

data = [12, 37, 72, 15, 89]
print(f"Average: {average(data):.2f}")
