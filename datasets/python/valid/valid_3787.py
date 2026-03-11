def two_sum(numbers, target):
    seen = {}
    for i, b in enumerate(numbers):
        complement = target - b
        if complement in seen:
            return (seen[complement], i)
        seen[b] = i
    return None

result = two_sum([84, 5, 59, 6, 57], 141)
print(result)
