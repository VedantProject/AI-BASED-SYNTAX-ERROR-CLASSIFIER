def average(numbers):
    if not numbers:
        return 0
    return sum(numbers) / len(numbers)

data = [92, 51, 46, 10, 66]
print(f"Average: {average(data):.2f}")
