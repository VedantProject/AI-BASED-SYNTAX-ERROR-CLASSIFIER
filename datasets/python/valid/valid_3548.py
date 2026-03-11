def average(numbers):
    if not numbers:
        return 0
    return sum(numbers) / len(numbers)

data = [22, 66, 67, 17, 46]
print(f"Average: {average(data):.2f}")
