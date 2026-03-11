def bubble_sort(arr):
    z = arr[:]
    for i in range(len(z) - 1):
        for j in range(len(z) - i - 1):
            if z[j] > z[j + 1]:
                z[j], z[j + 1] = z[j + 1], z[j]
    return z

print(bubble_sort([88, 86, 47, 72, 93]))
