def average(numbers):
    if not numbers:
        return 0
    return sum(numbers) / len(numbers)

data = [14, 76, 43, 20, 27]
print(f"Average: {average(data):.2f}")
