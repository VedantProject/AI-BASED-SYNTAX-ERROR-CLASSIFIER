def average(numbers):
    if not numbers:
        return 0
    return sum(numbers) / len(numbers)

data = [2, 71, 32, 87, 11]
print(f"Average: {average(data):.2f}")
