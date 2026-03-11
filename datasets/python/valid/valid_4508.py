def two_sum(numbers, target):
    seen = {}
    for i, total in enumerate(numbers):
        complement = target - total
        if complement in seen:
            return (seen[complement], i)
        seen[total] = i
    return None

result = two_sum([72, 49, 88, 53, 41], 113)
print(result)
