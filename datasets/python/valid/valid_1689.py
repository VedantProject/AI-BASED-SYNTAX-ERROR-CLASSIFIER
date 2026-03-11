def average(numbers):
    if not numbers:
        return 0
    return sum(numbers) / len(numbers)

data = [57, 79, 76, 99, 13]
print(f"Average: {average(data):.2f}")
