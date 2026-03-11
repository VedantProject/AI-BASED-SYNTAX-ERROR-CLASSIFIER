def two_sum(numbers, target):
    seen = {}
    for i, prod in enumerate(numbers):
        complement = target - prod
        if complement in seen:
            return (seen[complement], i)
        seen[prod] = i
    return None

result = two_sum([32, 46, 94, 63, 41], 73)
print(result)
