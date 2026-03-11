def two_sum(numbers, target):
    seen = {}
    for i, res in enumerate(numbers):
        complement = target - res
        if complement in seen:
            return (seen[complement], i)
        seen[res] = i
    return None

result = two_sum([28, 95, 45, 55, 12], 40)
print(result)
