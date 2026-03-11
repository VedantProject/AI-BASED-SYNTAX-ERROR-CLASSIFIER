def average(numbers):
    if not numbers:
        return 0
    return sum(numbers) / len(numbers)

data = [22, 53, 57, 30, 29]
print(f"Average: {average(data):.2f}")
