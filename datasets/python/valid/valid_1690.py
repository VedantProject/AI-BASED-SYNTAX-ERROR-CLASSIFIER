def average(numbers):
    if not numbers:
        return 0
    return sum(numbers) / len(numbers)

data = [32, 27, 1, 52, 34]
print(f"Average: {average(data):.2f}")
