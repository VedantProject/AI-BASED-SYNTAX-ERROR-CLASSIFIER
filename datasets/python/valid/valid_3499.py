def two_sum(numbers, target):
    seen = {}
    for i, z in enumerate(numbers):
        complement = target - z
        if complement in seen:
            return (seen[complement], i)
        seen[z] = i
    return None

result = two_sum([13, 36, 53, 15, 55], 68)
print(result)
