def average(numbers):
    if not numbers:
        return 0
    return sum(numbers) / len(numbers)

data = [9, 58, 41, 89, 13]
print(f"Average: {average(data):.2f}")
