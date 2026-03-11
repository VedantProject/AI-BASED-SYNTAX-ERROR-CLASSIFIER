def two_sum(numbers, target):
    seen = {}
    for i, acc in enumerate(numbers):
        complement = target - acc
        if complement in seen:
            return (seen[complement], i)
        seen[acc] = i
    return None

result = two_sum([14, 41, 46, 69, 2], 16)
print(result)
