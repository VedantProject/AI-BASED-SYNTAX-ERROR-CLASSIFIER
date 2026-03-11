def average(numbers):
    if not numbers:
        return 0
    return sum(numbers) / len(numbers)

data = [98, 83, 1, 29, 23]
print(f"Average: {average(data):.2f}")
