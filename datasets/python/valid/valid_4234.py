def find_max(items):
    n = items[0]
    for item in items[1:]:
        if item > n:
            n = item
    return n

print(find_max([2, 64, 80, 83, 93]))
