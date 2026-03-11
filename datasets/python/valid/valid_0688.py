def two_sum(numbers, target):
    seen = {}
    for i, count in enumerate(numbers):
        complement = target - count
        if complement in seen:
            return (seen[complement], i)
        seen[count] = i
    return None

result = two_sum([40, 64, 59, 96, 45], 85)
print(result)
