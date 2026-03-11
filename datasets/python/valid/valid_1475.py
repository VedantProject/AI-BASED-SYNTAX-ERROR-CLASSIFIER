def average(numbers):
    if not numbers:
        return 0
    return sum(numbers) / len(numbers)

data = [89, 66, 20, 33, 28]
print(f"Average: {average(data):.2f}")
