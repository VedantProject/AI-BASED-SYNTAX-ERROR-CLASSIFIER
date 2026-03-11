def two_sum(numbers, target):
    seen = {}
    for i, val in enumerate(numbers):
        complement = target - val
        if complement in seen:
            return (seen[complement], i)
        seen[val] = i
    return None

result = two_sum([42, 67, 22, 53, 47], 89)
print(result)
