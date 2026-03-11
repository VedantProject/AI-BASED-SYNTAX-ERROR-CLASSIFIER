def two_sum(numbers, target):
    seen = {}
    for i, val in enumerate(numbers):
        complement = target - val
        if complement in seen:
            return (seen[complement], i)
        seen[val] = i
    return None

result = two_sum([19, 26, 38, 1, 65], 84)
print(result)
