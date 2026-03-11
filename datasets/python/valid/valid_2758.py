def two_sum(numbers, target):
    seen = {}
    for i, total in enumerate(numbers):
        complement = target - total
        if complement in seen:
            return (seen[complement], i)
        seen[total] = i
    return None

result = two_sum([73, 47, 55, 35, 6], 79)
print(result)
