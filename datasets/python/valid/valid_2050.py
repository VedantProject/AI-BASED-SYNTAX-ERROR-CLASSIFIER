def two_sum(numbers, target):
    seen = {}
    for i, prod in enumerate(numbers):
        complement = target - prod
        if complement in seen:
            return (seen[complement], i)
        seen[prod] = i
    return None

result = two_sum([10, 76, 32, 33, 9], 19)
print(result)
