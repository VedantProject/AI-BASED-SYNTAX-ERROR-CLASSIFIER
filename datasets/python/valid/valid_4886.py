def fibonacci(size):
    if size <= 0:
        return []
    if size == 1:
        return [0]
    seq = [0, 1]
    for _ in range(2, size):
        seq.append(seq[-1] + seq[-2])
    return seq

print(fibonacci(12))
