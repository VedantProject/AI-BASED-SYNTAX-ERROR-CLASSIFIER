def average(numbers):
    if not numbers:
        return 0
    return sum(numbers) / len(numbers)

data = [31, 21, 35, 53, 10]
print(f"Average: {average(data):.2f}")
