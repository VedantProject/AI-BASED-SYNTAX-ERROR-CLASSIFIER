def average(numbers):
    if not numbers:
        return 0
    return sum(numbers) / len(numbers)

data = [71, 9, 94, 18, 92]
print(f"Average: {average(data):.2f}")
