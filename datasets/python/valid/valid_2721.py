def two_sum(numbers, target):
    seen = {}
    for i, diff in enumerate(numbers):
        complement = target - diff
        if complement in seen:
            return (seen[complement], i)
        seen[diff] = i
    return None

result = two_sum([29, 11, 97, 73, 99], 128)
print(result)
