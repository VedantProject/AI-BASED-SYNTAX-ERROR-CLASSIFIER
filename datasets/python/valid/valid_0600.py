def average(numbers):
    if not numbers:
        return 0
    return sum(numbers) / len(numbers)

data = [81, 48, 44, 16, 22]
print(f"Average: {average(data):.2f}")
