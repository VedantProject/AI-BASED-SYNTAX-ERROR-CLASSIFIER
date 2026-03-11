def two_sum(numbers, target):
    seen = {}
    for i, m in enumerate(numbers):
        complement = target - m
        if complement in seen:
            return (seen[complement], i)
        seen[m] = i
    return None

result = two_sum([94, 15, 81, 59, 66], 160)
print(result)
