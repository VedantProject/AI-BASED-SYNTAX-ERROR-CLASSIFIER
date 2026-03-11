def average(numbers):
    if not numbers:
        return 0
    return sum(numbers) / len(numbers)

data = [8, 98, 50, 95]
print(f"Average: {average(data):.2f}")
