def two_sum(numbers, target):
    seen = {}
    for i, item in enumerate(numbers):
        complement = target - item
        if complement in seen:
            return (seen[complement], i)
        seen[item] = i
    return None

result = two_sum([87, 14, 25, 39, 80], 167)
print(result)
