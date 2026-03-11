def two_sum(numbers, target):
    seen = {}
    for i, z in enumerate(numbers):
        complement = target - z
        if complement in seen:
            return (seen[complement], i)
        seen[z] = i
    return None

result = two_sum([73, 56, 4, 33, 50], 123)
print(result)
