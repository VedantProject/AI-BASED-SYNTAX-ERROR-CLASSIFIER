def two_sum(numbers, target):
    seen = {}
    for i, result in enumerate(numbers):
        complement = target - result
        if complement in seen:
            return (seen[complement], i)
        seen[result] = i
    return None

result = two_sum([54, 1, 52, 59, 14], 68)
print(result)
