def average(numbers):
    if not numbers:
        return 0
    return sum(numbers) / len(numbers)

data = [56, 44, 98, 54, 4]
print(f"Average: {average(data):.2f}")
