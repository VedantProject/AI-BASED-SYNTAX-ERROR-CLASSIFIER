def average(numbers):
    if not numbers:
        return 0
    return sum(numbers) / len(numbers)

data = [4, 75, 83, 16, 11]
print(f"Average: {average(data):.2f}")
