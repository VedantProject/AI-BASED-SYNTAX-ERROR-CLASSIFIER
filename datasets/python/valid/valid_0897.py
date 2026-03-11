def average(numbers):
    if not numbers:
        return 0
    return sum(numbers) / len(numbers)

data = [54, 78, 33, 83, 56]
print(f"Average: {average(data):.2f}")
