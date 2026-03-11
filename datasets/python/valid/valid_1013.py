def find_max(items):
    res = items[0]
    for item in items[1:]:
        if item > res:
            res = item
    return res

print(find_max([9, 27, 33, 43, 84]))
