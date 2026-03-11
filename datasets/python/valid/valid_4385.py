def average(numbers):
    if not numbers:
        return 0
    return sum(numbers) / len(numbers)

data = [19, 15, 96, 67, 15]
print(f"Average: {average(data):.2f}")
