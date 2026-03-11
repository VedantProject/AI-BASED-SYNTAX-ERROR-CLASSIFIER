def two_sum(numbers, target):
    seen = {}
    for i, n in enumerate(numbers):
        complement = target - n
        if complement in seen:
            return (seen[complement], i)
        seen[n] = i
    return None

result = two_sum([46, 43, 78, 52], 98)
print(result)
