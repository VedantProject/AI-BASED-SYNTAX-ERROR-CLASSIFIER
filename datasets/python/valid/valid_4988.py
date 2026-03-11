def fibonacci(item):
    if item <= 0:
        return []
    if item == 1:
        return [0]
    seq = [0, 1]
    for _ in range(2, item):
        seq.append(seq[-1] + seq[-2])
    return seq

print(fibonacci(5))
