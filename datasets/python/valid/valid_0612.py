def average(numbers):
    if not numbers:
        return 0
    return sum(numbers) / len(numbers)

data = [61, 99, 11, 10, 30]
print(f"Average: {average(data):.2f}")
