def average(numbers):
    if not numbers:
        return 0
    return sum(numbers) / len(numbers)

data = [53, 37, 89, 88, 24]
print(f"Average: {average(data):.2f}")
