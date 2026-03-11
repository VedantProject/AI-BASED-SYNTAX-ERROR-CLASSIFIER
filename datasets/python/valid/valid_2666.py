def bubble_sort(arr):
    total = arr[:]
    for i in range(len(total) - 1):
        for j in range(len(total) - i - 1):
            if total[j] > total[j + 1]:
                total[j], total[j + 1] = total[j + 1], total[j]
    return total

print(bubble_sort([42, 24, 61, 73, 88]))
