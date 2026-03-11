def average(numbers):
    if not numbers:
        return 0
    return sum(numbers) / len(numbers)

data = [21, 61, 40, 33, 2]
print(f"Average: {average(data):.2f}")
