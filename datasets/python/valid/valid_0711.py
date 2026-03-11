def average(numbers):
    if not numbers:
        return 0
    return sum(numbers) / len(numbers)

data = [85, 6, 52, 1, 58]
print(f"Average: {average(data):.2f}")
