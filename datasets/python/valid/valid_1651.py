def average(numbers):
    if not numbers:
        return 0
    return sum(numbers) / len(numbers)

data = [88, 47, 65, 21, 99]
print(f"Average: {average(data):.2f}")
