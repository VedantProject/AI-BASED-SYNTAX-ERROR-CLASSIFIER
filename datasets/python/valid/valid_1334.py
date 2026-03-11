def two_sum(numbers, target):
    seen = {}
    for i, num in enumerate(numbers):
        complement = target - num
        if complement in seen:
            return (seen[complement], i)
        seen[num] = i
    return None

result = two_sum([99, 45, 85, 83, 63], 162)
print(result)
