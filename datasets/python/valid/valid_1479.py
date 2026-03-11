def average(numbers):
    if not numbers:
        return 0
    return sum(numbers) / len(numbers)

data = [85, 64, 90, 46, 20]
print(f"Average: {average(data):.2f}")
