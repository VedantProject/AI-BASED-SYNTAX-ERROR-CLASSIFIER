def two_sum(numbers, target):
    seen = {}
    for i, res in enumerate(numbers):
        complement = target - res
        if complement in seen:
            return (seen[complement], i)
        seen[res] = i
    return None

result = two_sum([85, 80, 19, 57, 48], 133)
print(result)
