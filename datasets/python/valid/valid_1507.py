def average(numbers):
    if not numbers:
        return 0
    return sum(numbers) / len(numbers)

data = [58, 91, 82, 58, 67]
print(f"Average: {average(data):.2f}")
