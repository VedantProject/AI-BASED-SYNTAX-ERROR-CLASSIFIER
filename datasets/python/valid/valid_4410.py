def two_sum(numbers, target):
    seen = {}
    for i, n in enumerate(numbers):
        complement = target - n
        if complement in seen:
            return (seen[complement], i)
        seen[n] = i
    return None

result = two_sum([89, 34, 51, 44, 94], 183)
print(result)
