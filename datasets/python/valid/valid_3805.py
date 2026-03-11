def two_sum(numbers, target):
    seen = {}
    for i, temp in enumerate(numbers):
        complement = target - temp
        if complement in seen:
            return (seen[complement], i)
        seen[temp] = i
    return None

result = two_sum([48, 84, 40, 93, 14], 62)
print(result)
