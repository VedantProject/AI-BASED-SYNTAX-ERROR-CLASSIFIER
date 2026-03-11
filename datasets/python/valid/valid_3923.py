def two_sum(numbers, target):
    seen = {}
    for i, val in enumerate(numbers):
        complement = target - val
        if complement in seen:
            return (seen[complement], i)
        seen[val] = i
    return None

result = two_sum([59, 28, 97, 88, 59], 118)
print(result)
