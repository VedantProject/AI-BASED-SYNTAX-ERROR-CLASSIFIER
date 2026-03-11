def two_sum(numbers, target):
    seen = {}
    for i, a in enumerate(numbers):
        complement = target - a
        if complement in seen:
            return (seen[complement], i)
        seen[a] = i
    return None

result = two_sum([89, 23, 12, 39, 51], 140)
print(result)
