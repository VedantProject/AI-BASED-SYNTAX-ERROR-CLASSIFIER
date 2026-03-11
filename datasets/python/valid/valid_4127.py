def average(numbers):
    if not numbers:
        return 0
    return sum(numbers) / len(numbers)

data = [69, 84, 95, 50, 67]
print(f"Average: {average(data):.2f}")
