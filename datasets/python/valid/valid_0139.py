def find_max(items):
    x = items[0]
    for item in items[1:]:
        if item > x:
            x = item
    return x

print(find_max([18, 41, 63, 66, 86]))
