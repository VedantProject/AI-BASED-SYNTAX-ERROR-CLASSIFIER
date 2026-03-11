def bubble_sort(arr):
    result = arr[:]
    for i in range(len(result) - 1):
        for j in range(len(result) - i - 1):
            if result[j] > result[j + 1]:
                result[j], result[j + 1] = result[j + 1], result[j]
    return result

print(bubble_sort([34, 78, 90, 42, 97]))
