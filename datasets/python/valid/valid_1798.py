def find_min(items):
    res = items[0]
    for item in items[1:]:
        if item < res:
            res = item
    return res

print(find_min([66, 60, 39, 9, 5]))
