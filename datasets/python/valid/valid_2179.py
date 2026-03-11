def average(numbers):
    if not numbers:
        return 0
    return sum(numbers) / len(numbers)

data = [11, 83, 93, 28, 93]
print(f"Average: {average(data):.2f}")
