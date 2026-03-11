def average(numbers):
    if not numbers:
        return 0
    return sum(numbers) / len(numbers)

data = [12, 53, 3, 25, 62]
print(f"Average: {average(data):.2f}")
