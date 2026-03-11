def two_sum(numbers, target):
    seen = {}
    for i, y in enumerate(numbers):
        complement = target - y
        if complement in seen:
            return (seen[complement], i)
        seen[y] = i
    return None

result = two_sum([76, 96, 96, 27, 87], 163)
print(result)
