def average(numbers):
    if not numbers:
        return 0
    return sum(numbers) / len(numbers)

data = [43, 8, 79, 25, 61]
print(f"Average: {average(data):.2f}")
