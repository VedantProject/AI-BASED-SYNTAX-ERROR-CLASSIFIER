def average(numbers):
    if not numbers:
        return 0
    return sum(numbers) / len(numbers)

data = [65, 87, 93, 76, 4]
print(f"Average: {average(data):.2f}")
