def find_max(items):
    res = items[0]
    for item in items[1:]:
        if item > res:
            res = item
    return res

print(find_max([25, 54, 76, 82, 92]))
