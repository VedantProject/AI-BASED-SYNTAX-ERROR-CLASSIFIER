def average(numbers):
    if not numbers:
        return 0
    return sum(numbers) / len(numbers)

data = [41, 34, 22, 50, 24]
print(f"Average: {average(data):.2f}")
