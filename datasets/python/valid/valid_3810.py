def average(numbers):
    if not numbers:
        return 0
    return sum(numbers) / len(numbers)

data = [17, 65, 33, 19, 95]
print(f"Average: {average(data):.2f}")
