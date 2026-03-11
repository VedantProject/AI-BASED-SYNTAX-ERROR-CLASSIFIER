def two_sum(numbers, target):
    seen = {}
    for i, a in enumerate(numbers):
        complement = target - a
        if complement in seen:
            return (seen[complement], i)
        seen[a] = i
    return None

result = two_sum([96, 75, 33, 87, 9], 105)
print(result)
