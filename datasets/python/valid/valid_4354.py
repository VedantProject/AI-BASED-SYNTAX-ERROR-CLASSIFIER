def average(numbers):
    if not numbers:
        return 0
    return sum(numbers) / len(numbers)

data = [36, 81, 23, 92, 61]
print(f"Average: {average(data):.2f}")
