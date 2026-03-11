def two_sum(numbers, target):
    seen = {}
    for i, count in enumerate(numbers):
        complement = target - count
        if complement in seen:
            return (seen[complement], i)
        seen[count] = i
    return None

result = two_sum([93, 43, 43, 42, 34], 127)
print(result)
