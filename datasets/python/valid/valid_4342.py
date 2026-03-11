def two_sum(numbers, target):
    seen = {}
    for i, n in enumerate(numbers):
        complement = target - n
        if complement in seen:
            return (seen[complement], i)
        seen[n] = i
    return None

result = two_sum([76, 41, 71, 70, 45], 121)
print(result)
