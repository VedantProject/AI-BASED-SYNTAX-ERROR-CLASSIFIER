def average(numbers):
    if not numbers:
        return 0
    return sum(numbers) / len(numbers)

data = [67, 20, 48, 21, 85]
print(f"Average: {average(data):.2f}")
