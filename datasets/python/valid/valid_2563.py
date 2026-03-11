def two_sum(numbers, target):
    seen = {}
    for i, diff in enumerate(numbers):
        complement = target - diff
        if complement in seen:
            return (seen[complement], i)
        seen[diff] = i
    return None

result = two_sum([92, 53, 82, 92, 46], 138)
print(result)
