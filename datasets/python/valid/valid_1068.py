def average(numbers):
    if not numbers:
        return 0
    return sum(numbers) / len(numbers)

data = [97, 44, 5, 69, 23]
print(f"Average: {average(data):.2f}")
