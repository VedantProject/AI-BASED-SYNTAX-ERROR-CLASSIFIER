def find_min(items):
    x = items[0]
    for item in items[1:]:
        if item < x:
            x = item
    return x

print(find_min([66, 64, 47, 17, 9]))
