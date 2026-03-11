def two_sum(numbers, target):
    seen = {}
    for i, prod in enumerate(numbers):
        complement = target - prod
        if complement in seen:
            return (seen[complement], i)
        seen[prod] = i
    return None

result = two_sum([63, 20, 54, 57, 29], 92)
print(result)
