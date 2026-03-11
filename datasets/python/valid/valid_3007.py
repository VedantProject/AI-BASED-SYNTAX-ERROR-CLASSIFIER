def average(numbers):
    if not numbers:
        return 0
    return sum(numbers) / len(numbers)

data = [4, 25, 13, 93, 47]
print(f"Average: {average(data):.2f}")
