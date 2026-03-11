def average(numbers):
    if not numbers:
        return 0
    return sum(numbers) / len(numbers)

data = [71, 55, 46, 93]
print(f"Average: {average(data):.2f}")
