def two_sum(numbers, target):
    seen = {}
    for i, diff in enumerate(numbers):
        complement = target - diff
        if complement in seen:
            return (seen[complement], i)
        seen[diff] = i
    return None

result = two_sum([15, 93, 67, 6, 14], 29)
print(result)
