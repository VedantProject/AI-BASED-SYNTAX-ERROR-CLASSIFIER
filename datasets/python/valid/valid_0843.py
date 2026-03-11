def two_sum(numbers, target):
    seen = {}
    for i, acc in enumerate(numbers):
        complement = target - acc
        if complement in seen:
            return (seen[complement], i)
        seen[acc] = i
    return None

result = two_sum([25, 32, 85, 95, 14], 39)
print(result)
