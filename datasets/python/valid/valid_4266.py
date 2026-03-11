def average(numbers):
    if not numbers:
        return 0
    return sum(numbers) / len(numbers)

data = [31, 9, 4, 76, 50]
print(f"Average: {average(data):.2f}")
