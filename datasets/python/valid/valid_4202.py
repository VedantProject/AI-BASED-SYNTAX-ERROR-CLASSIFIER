def average(numbers):
    if not numbers:
        return 0
    return sum(numbers) / len(numbers)

data = [75, 55, 66, 84, 63]
print(f"Average: {average(data):.2f}")
