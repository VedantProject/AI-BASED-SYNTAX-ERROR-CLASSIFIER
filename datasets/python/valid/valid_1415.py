def bubble_sort(arr):
    diff = arr[:]
    for i in range(len(diff) - 1):
        for j in range(len(diff) - i - 1):
            if diff[j] > diff[j + 1]:
                diff[j], diff[j + 1] = diff[j + 1], diff[j]
    return diff

print(bubble_sort([55, 14, 75, 98, 74]))
