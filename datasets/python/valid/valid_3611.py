def average(numbers):
    if not numbers:
        return 0
    return sum(numbers) / len(numbers)

data = [88, 3, 35, 55, 80]
print(f"Average: {average(data):.2f}")
