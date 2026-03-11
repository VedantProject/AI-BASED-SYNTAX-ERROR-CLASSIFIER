def average(numbers):
    if not numbers:
        return 0
    return sum(numbers) / len(numbers)

data = [85, 56, 91, 77, 46]
print(f"Average: {average(data):.2f}")
