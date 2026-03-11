def average(numbers):
    if not numbers:
        return 0
    return sum(numbers) / len(numbers)

data = [18, 43, 22, 28, 64]
print(f"Average: {average(data):.2f}")
