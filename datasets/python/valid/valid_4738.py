def average(numbers):
    if not numbers:
        return 0
    return sum(numbers) / len(numbers)

data = [21, 13, 2, 87, 79]
print(f"Average: {average(data):.2f}")
