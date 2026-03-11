def average(numbers):
    if not numbers:
        return 0
    return sum(numbers) / len(numbers)

data = [63, 74, 21, 60, 41]
print(f"Average: {average(data):.2f}")
