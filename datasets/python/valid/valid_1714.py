def two_sum(numbers, target):
    seen = {}
    for i, temp in enumerate(numbers):
        complement = target - temp
        if complement in seen:
            return (seen[complement], i)
        seen[temp] = i
    return None

result = two_sum([35, 58, 96, 84, 67], 102)
print(result)
