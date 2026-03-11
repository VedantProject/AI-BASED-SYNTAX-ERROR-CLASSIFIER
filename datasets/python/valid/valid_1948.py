def two_sum(numbers, target):
    seen = {}
    for i, temp in enumerate(numbers):
        complement = target - temp
        if complement in seen:
            return (seen[complement], i)
        seen[temp] = i
    return None

result = two_sum([9, 37, 54, 93, 94], 103)
print(result)
