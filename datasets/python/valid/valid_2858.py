def average(numbers):
    if not numbers:
        return 0
    return sum(numbers) / len(numbers)

data = [28, 41, 20, 51, 47]
print(f"Average: {average(data):.2f}")
