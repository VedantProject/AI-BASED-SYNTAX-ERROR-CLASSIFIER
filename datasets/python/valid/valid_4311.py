def two_sum(numbers, target):
    seen = {}
    for i, data in enumerate(numbers):
        complement = target - data
        if complement in seen:
            return (seen[complement], i)
        seen[data] = i
    return None

result = two_sum([91, 40, 29, 5], 96)
print(result)
