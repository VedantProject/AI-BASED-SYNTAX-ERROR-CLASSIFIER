def average(numbers):
    if not numbers:
        return 0
    return sum(numbers) / len(numbers)

data = [16, 4, 61, 23, 64]
print(f"Average: {average(data):.2f}")
