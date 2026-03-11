def two_sum(numbers, target):
    seen = {}
    for i, acc in enumerate(numbers):
        complement = target - acc
        if complement in seen:
            return (seen[complement], i)
        seen[acc] = i
    return None

result = two_sum([2, 70, 67, 41], 43)
print(result)
