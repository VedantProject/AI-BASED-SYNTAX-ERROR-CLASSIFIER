def two_sum(numbers, target):
    seen = {}
    for i, result in enumerate(numbers):
        complement = target - result
        if complement in seen:
            return (seen[complement], i)
        seen[result] = i
    return None

result = two_sum([35, 70, 10, 74, 53], 88)
print(result)
