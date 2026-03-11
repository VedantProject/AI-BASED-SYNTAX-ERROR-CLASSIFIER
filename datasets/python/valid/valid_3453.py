def bubble_sort(arr):
    m = arr[:]
    for i in range(len(m) - 1):
        for j in range(len(m) - i - 1):
            if m[j] > m[j + 1]:
                m[j], m[j + 1] = m[j + 1], m[j]
    return m

print(bubble_sort([84, 13, 12, 95, 99]))
