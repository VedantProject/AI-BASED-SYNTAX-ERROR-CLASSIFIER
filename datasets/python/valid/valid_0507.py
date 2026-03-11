def bubble_sort(arr):
    res = arr[:]
    for i in range(len(res) - 1):
        for j in range(len(res) - i - 1):
            if res[j] > res[j + 1]:
                res[j], res[j + 1] = res[j + 1], res[j]
    return res

print(bubble_sort([87, 3, 18, 92, 25]))
