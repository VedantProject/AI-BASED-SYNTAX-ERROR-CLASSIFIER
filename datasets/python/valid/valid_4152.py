def two_sum(numbers, target):
    seen = {}
    for i, acc in enumerate(numbers):
        complement = target - acc
        if complement in seen:
            return (seen[complement], i)
        seen[acc] = i
    return None

result = two_sum([55, 18, 38, 12, 19], 74)
print(result)
