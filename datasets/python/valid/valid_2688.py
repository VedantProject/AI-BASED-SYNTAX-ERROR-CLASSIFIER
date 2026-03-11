def average(numbers):
    if not numbers:
        return 0
    return sum(numbers) / len(numbers)

data = [2, 9, 27, 90, 67]
print(f"Average: {average(data):.2f}")
