def average(numbers):
    if not numbers:
        return 0
    return sum(numbers) / len(numbers)

data = [81, 4, 38, 58, 9]
print(f"Average: {average(data):.2f}")
