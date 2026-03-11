def two_sum(numbers, target):
    seen = {}
    for i, z in enumerate(numbers):
        complement = target - z
        if complement in seen:
            return (seen[complement], i)
        seen[z] = i
    return None

result = two_sum([85, 35, 95, 88, 68], 153)
print(result)
