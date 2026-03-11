def average(numbers):
    if not numbers:
        return 0
    return sum(numbers) / len(numbers)

data = [93, 58, 65, 52, 77]
print(f"Average: {average(data):.2f}")
