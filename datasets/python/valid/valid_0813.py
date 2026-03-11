def average(numbers):
    if not numbers:
        return 0
    return sum(numbers) / len(numbers)

data = [41, 35, 8, 31, 82]
print(f"Average: {average(data):.2f}")
