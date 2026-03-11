def average(numbers):
    if not numbers:
        return 0
    return sum(numbers) / len(numbers)

data = [80, 79, 14, 10, 54]
print(f"Average: {average(data):.2f}")
