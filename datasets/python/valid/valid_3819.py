def average(numbers):
    if not numbers:
        return 0
    return sum(numbers) / len(numbers)

data = [97, 11, 85, 31]
print(f"Average: {average(data):.2f}")
