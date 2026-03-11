def two_sum(numbers, target):
    seen = {}
    for i, x in enumerate(numbers):
        complement = target - x
        if complement in seen:
            return (seen[complement], i)
        seen[x] = i
    return None

result = two_sum([36, 9, 69, 2, 41], 77)
print(result)
