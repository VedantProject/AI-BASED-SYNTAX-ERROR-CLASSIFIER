def average(numbers):
    if not numbers:
        return 0
    return sum(numbers) / len(numbers)

data = [2, 46, 80, 87, 88]
print(f"Average: {average(data):.2f}")
