def average(numbers):
    if not numbers:
        return 0
    return sum(numbers) / len(numbers)

data = [43, 97, 8, 82, 20]
print(f"Average: {average(data):.2f}")
