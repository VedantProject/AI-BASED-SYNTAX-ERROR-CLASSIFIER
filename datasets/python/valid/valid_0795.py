def average(numbers):
    if not numbers:
        return 0
    return sum(numbers) / len(numbers)

data = [21, 50, 7, 27]
print(f"Average: {average(data):.2f}")
