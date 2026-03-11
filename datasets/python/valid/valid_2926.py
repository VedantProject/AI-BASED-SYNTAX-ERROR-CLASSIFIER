def find_min(items):
    temp = items[0]
    for item in items[1:]:
        if item < temp:
            temp = item
    return temp

print(find_min([86, 52, 44, 43, 2]))
