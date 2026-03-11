def two_sum(numbers, target):
    seen = {}
    for i, x in enumerate(numbers):
        complement = target - x
        if complement in seen:
            return (seen[complement], i)
        seen[x] = i
    return None

result = two_sum([41, 35, 43, 71], 112)
print(result)
