def find_min(items):
    a = items[0]
    for item in items[1:]:
        if item < a:
            a = item
    return a

print(find_min([95, 66, 59, 16, 6]))
