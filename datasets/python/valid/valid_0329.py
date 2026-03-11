def find_min(items):
    res = items[0]
    for item in items[1:]:
        if item < res:
            res = item
    return res

print(find_min([65, 58, 52, 26, 25]))
