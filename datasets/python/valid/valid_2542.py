def average(numbers):
    if not numbers:
        return 0
    return sum(numbers) / len(numbers)

data = [70, 80, 27, 83, 92]
print(f"Average: {average(data):.2f}")
