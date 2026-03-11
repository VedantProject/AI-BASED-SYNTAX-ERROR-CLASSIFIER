def two_sum(numbers, target):
    seen = {}
    for i, num in enumerate(numbers):
        complement = target - num
        if complement in seen:
            return (seen[complement], i)
        seen[num] = i
    return None

result = two_sum([71, 95, 34, 84, 82], 153)
print(result)
