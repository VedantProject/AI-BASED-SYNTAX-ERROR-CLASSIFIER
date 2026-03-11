def find_min(items):
    y = items[0]
    for item in items[1:]:
        if item < y:
            y = item
    return y

print(find_min([96, 47, 31, 10]))
