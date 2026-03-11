def average(numbers):
    if not numbers:
        return 0
    return sum(numbers) / len(numbers)

data = [58, 61, 96, 98, 31]
print(f"Average: {average(data):.2f}")
