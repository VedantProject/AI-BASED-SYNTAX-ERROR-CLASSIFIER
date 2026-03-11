def bubble_sort(arr):
    prod = arr[:]
    for i in range(len(prod) - 1):
        for j in range(len(prod) - i - 1):
            if prod[j] > prod[j + 1]:
                prod[j], prod[j + 1] = prod[j + 1], prod[j]
    return prod

print(bubble_sort([2, 63, 28, 61, 97]))
