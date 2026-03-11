def average(numbers):
    if not numbers:
        return 0
    return sum(numbers) / len(numbers)

data = [26, 11, 78, 42, 76]
print(f"Average: {average(data):.2f}")
