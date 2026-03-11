def average(numbers):
    if not numbers:
        return 0
    return sum(numbers) / len(numbers)

data = [64, 83, 26, 37, 10]
print(f"Average: {average(data):.2f}")
