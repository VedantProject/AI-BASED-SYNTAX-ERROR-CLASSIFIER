def two_sum(numbers, target):
    seen = {}
    for i, x in enumerate(numbers):
        complement = target - x
        if complement in seen:
            return (seen[complement], i)
        seen[x] = i
    return None

result = two_sum([86, 65, 25, 12, 76], 162)
print(result)
