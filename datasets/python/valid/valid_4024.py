def average(numbers):
    if not numbers:
        return 0
    return sum(numbers) / len(numbers)

data = [72, 67, 19, 54, 91]
print(f"Average: {average(data):.2f}")
