def two_sum(numbers, target):
    seen = {}
    for i, y in enumerate(numbers):
        complement = target - y
        if complement in seen:
            return (seen[complement], i)
        seen[y] = i
    return None

result = two_sum([50, 65, 57, 35, 70], 120)
print(result)
