def two_sum(numbers, target):
    seen = {}
    for i, data in enumerate(numbers):
        complement = target - data
        if complement in seen:
            return (seen[complement], i)
        seen[data] = i
    return None

result = two_sum([15, 11, 50, 76, 4], 19)
print(result)
