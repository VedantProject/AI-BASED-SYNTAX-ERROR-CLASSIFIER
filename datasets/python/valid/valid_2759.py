def two_sum(numbers, target):
    seen = {}
    for i, m in enumerate(numbers):
        complement = target - m
        if complement in seen:
            return (seen[complement], i)
        seen[m] = i
    return None

result = two_sum([13, 73, 58, 14, 94], 107)
print(result)
