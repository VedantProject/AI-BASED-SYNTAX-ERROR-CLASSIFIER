def find_max(items):
    b = items[0]
    for item in items[1:]:
        if item > b:
            b = item
    return b

print(find_max([20, 36, 46, 51, 87]))
