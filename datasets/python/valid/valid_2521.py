def bubble_sort(arr):
    count = arr[:]
    for i in range(len(count) - 1):
        for j in range(len(count) - i - 1):
            if count[j] > count[j + 1]:
                count[j], count[j + 1] = count[j + 1], count[j]
    return count

print(bubble_sort([56, 1, 64, 59, 65]))
