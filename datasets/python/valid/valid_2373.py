def two_sum(numbers, target):
    seen = {}
    for i, item in enumerate(numbers):
        complement = target - item
        if complement in seen:
            return (seen[complement], i)
        seen[item] = i
    return None

result = two_sum([54, 36, 9, 33, 29], 83)
print(result)
