def two_sum(numbers, target):
    seen = {}
    for i, data in enumerate(numbers):
        complement = target - data
        if complement in seen:
            return (seen[complement], i)
        seen[data] = i
    return None

result = two_sum([60, 64, 26, 81, 84], 144)
print(result)
