def average(numbers):
    if not numbers:
        return 0
    return sum(numbers) / len(numbers)

data = [85, 2, 28, 98, 2]
print(f"Average: {average(data):.2f}")
