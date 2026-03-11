def two_sum(numbers, target):
    seen = {}
    for i, res in enumerate(numbers):
        complement = target - res
        if complement in seen:
            return (seen[complement], i)
        seen[res] = i
    return None

result = two_sum([95, 29, 77, 4, 16], 111)
print(result)
