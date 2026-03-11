def average(numbers):
    if not numbers:
        return 0
    return sum(numbers) / len(numbers)

data = [8, 53, 29, 63, 67]
print(f"Average: {average(data):.2f}")
