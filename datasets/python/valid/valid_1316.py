def average(numbers):
    if not numbers:
        return 0
    return sum(numbers) / len(numbers)

data = [72, 17, 4, 47, 32]
print(f"Average: {average(data):.2f}")
