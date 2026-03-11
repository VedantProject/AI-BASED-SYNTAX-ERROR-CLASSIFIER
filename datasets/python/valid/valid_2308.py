def two_sum(numbers, target):
    seen = {}
    for i, num in enumerate(numbers):
        complement = target - num
        if complement in seen:
            return (seen[complement], i)
        seen[num] = i
    return None

result = two_sum([25, 10, 55, 77, 49], 74)
print(result)
