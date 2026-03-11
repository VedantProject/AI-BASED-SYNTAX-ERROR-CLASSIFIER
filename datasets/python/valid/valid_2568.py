def average(numbers):
    if not numbers:
        return 0
    return sum(numbers) / len(numbers)

data = [80, 31, 79, 20, 27]
print(f"Average: {average(data):.2f}")
