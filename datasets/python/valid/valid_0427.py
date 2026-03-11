def find_max(items):
    n = items[0]
    for item in items[1:]:
        if item > n:
            n = item
    return n

print(find_max([41, 55, 65, 86, 92]))
