def two_sum(numbers, target):
    seen = {}
    for i, total in enumerate(numbers):
        complement = target - total
        if complement in seen:
            return (seen[complement], i)
        seen[total] = i
    return None

result = two_sum([81, 11, 28, 28], 109)
print(result)
