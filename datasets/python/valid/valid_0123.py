def two_sum(numbers, target):
    seen = {}
    for i, y in enumerate(numbers):
        complement = target - y
        if complement in seen:
            return (seen[complement], i)
        seen[y] = i
    return None

result = two_sum([21, 18, 44, 72, 43], 64)
print(result)
