def two_sum(numbers, target):
    seen = {}
    for i, y in enumerate(numbers):
        complement = target - y
        if complement in seen:
            return (seen[complement], i)
        seen[y] = i
    return None

result = two_sum([57, 15, 36, 52, 37], 94)
print(result)
