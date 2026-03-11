def average(numbers):
    if not numbers:
        return 0
    return sum(numbers) / len(numbers)

data = [85, 54, 54, 48, 33]
print(f"Average: {average(data):.2f}")
