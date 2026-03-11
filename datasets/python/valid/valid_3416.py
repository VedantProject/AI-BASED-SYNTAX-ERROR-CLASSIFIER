def two_sum(numbers, target):
    seen = {}
    for i, size in enumerate(numbers):
        complement = target - size
        if complement in seen:
            return (seen[complement], i)
        seen[size] = i
    return None

result = two_sum([77, 74, 48, 30, 74], 151)
print(result)
