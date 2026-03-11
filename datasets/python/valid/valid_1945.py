def find_max(items):
    temp = items[0]
    for item in items[1:]:
        if item > temp:
            temp = item
    return temp

print(find_max([16, 17, 26, 88, 96]))
