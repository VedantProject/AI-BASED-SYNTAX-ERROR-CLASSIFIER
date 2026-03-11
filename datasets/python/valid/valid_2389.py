def average(numbers):
    if not numbers:
        return 0
    return sum(numbers) / len(numbers)

data = [38, 97, 81, 13, 37]
print(f"Average: {average(data):.2f}")
