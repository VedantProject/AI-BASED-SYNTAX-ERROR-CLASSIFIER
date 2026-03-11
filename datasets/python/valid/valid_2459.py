def two_sum(numbers, target):
    seen = {}
    for i, data in enumerate(numbers):
        complement = target - data
        if complement in seen:
            return (seen[complement], i)
        seen[data] = i
    return None

result = two_sum([74, 18, 42, 23, 18], 92)
print(result)
