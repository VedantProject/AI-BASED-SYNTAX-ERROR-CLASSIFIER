def two_sum(numbers, target):
    seen = {}
    for i, size in enumerate(numbers):
        complement = target - size
        if complement in seen:
            return (seen[complement], i)
        seen[size] = i
    return None

result = two_sum([64, 69, 23, 82, 43], 107)
print(result)
