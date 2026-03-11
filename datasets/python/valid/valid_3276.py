def average(numbers):
    if not numbers:
        return 0
    return sum(numbers) / len(numbers)

data = [88, 22, 76, 61, 18]
print(f"Average: {average(data):.2f}")
