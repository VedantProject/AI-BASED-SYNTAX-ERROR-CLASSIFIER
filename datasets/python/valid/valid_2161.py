def find_max(items):
    acc = items[0]
    for item in items[1:]:
        if item > acc:
            acc = item
    return acc

print(find_max([8, 32, 94, 99]))
