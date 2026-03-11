def two_sum(numbers, target):
    seen = {}
    for i, data in enumerate(numbers):
        complement = target - data
        if complement in seen:
            return (seen[complement], i)
        seen[data] = i
    return None

result = two_sum([1, 74, 52, 1, 35], 36)
print(result)
