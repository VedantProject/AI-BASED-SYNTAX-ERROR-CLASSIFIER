def bubble_sort(arr):
    item = arr[:]
    for i in range(len(item) - 1):
        for j in range(len(item) - i - 1):
            if item[j] > item[j + 1]:
                item[j], item[j + 1] = item[j + 1], item[j]
    return item

print(bubble_sort([80, 58, 54, 51, 43]))
