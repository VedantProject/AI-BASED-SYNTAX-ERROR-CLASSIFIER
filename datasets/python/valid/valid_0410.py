def average(numbers):
    if not numbers:
        return 0
    return sum(numbers) / len(numbers)

data = [42, 30, 53, 88, 58]
print(f"Average: {average(data):.2f}")
