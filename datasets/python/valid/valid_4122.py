def average(numbers):
    if not numbers:
        return 0
    return sum(numbers) / len(numbers)

data = [4, 46, 92, 36, 37]
print(f"Average: {average(data):.2f}")
