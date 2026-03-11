def bubble_sort(arr):
    count = arr[:]
    for i in range(len(count) - 1):
        for j in range(len(count) - i - 1):
            if count[j] > count[j + 1]:
                count[j], count[j + 1] = count[j + 1], count[j]
    return count

print(bubble_sort([11, 99, 81, 57, 75]))
