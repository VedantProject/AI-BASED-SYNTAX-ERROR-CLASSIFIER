def average(numbers):
    if not numbers:
        return 0
    return sum(numbers) / len(numbers)

data = [30, 20, 53, 84, 70]
print(f"Average: {average(data):.2f}")
