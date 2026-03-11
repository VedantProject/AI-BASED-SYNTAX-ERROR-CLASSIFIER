def two_sum(numbers, target):
    seen = {}
    for i, val in enumerate(numbers):
        complement = target - val
        if complement in seen:
            return (seen[complement], i)
        seen[val] = i
    return None

result = two_sum([80, 24, 47, 21, 55], 135)
print(result)
