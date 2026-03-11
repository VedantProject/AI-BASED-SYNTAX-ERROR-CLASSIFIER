def average(numbers):
    if not numbers:
        return 0
    return sum(numbers) / len(numbers)

data = [49, 99, 38, 23, 51]
print(f"Average: {average(data):.2f}")
