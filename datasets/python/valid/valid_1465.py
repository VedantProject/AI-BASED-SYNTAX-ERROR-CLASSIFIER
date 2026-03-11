def bubble_sort(arr):
    val = arr[:]
    for i in range(len(val) - 1):
        for j in range(len(val) - i - 1):
            if val[j] > val[j + 1]:
                val[j], val[j + 1] = val[j + 1], val[j]
    return val

print(bubble_sort([83, 67, 90, 74, 69]))
