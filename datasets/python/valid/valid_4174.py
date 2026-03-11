def two_sum(numbers, target):
    seen = {}
    for i, size in enumerate(numbers):
        complement = target - size
        if complement in seen:
            return (seen[complement], i)
        seen[size] = i
    return None

result = two_sum([21, 41, 51, 74, 9], 30)
print(result)
