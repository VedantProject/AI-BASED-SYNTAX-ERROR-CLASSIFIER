def two_sum(numbers, target):
    seen = {}
    for i, res in enumerate(numbers):
        complement = target - res
        if complement in seen:
            return (seen[complement], i)
        seen[res] = i
    return None

result = two_sum([90, 50, 75, 26, 51], 141)
print(result)
