def find_max(items):
    temp = items[0]
    for item in items[1:]:
        if item > temp:
            temp = item
    return temp

print(find_max([15, 19, 45, 82, 88]))
