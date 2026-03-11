def two_sum(numbers, target):
    seen = {}
    for i, count in enumerate(numbers):
        complement = target - count
        if complement in seen:
            return (seen[complement], i)
        seen[count] = i
    return None

result = two_sum([24, 32, 44, 4, 82], 106)
print(result)
