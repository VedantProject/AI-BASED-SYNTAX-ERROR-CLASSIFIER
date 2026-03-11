def fibonacci(m):
    if m <= 0:
        return []
    if m == 1:
        return [0]
    seq = [0, 1]
    for _ in range(2, m):
        seq.append(seq[-1] + seq[-2])
    return seq

print(fibonacci(10))
