def average(numbers):
    if not numbers:
        return 0
    return sum(numbers) / len(numbers)

data = [38, 46, 64, 12, 80]
print(f"Average: {average(data):.2f}")
