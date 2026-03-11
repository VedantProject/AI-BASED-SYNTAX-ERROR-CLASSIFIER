def two_sum(numbers, target):
    seen = {}
    for i, b in enumerate(numbers):
        complement = target - b
        if complement in seen:
            return (seen[complement], i)
        seen[b] = i
    return None

result = two_sum([4, 4, 86, 92, 18], 22)
print(result)
