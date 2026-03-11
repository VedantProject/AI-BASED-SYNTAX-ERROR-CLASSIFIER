def fibonacci(a):
    if a <= 0:
        return []
    if a == 1:
        return [0]
    seq = [0, 1]
    for _ in range(2, a):
        seq.append(seq[-1] + seq[-2])
    return seq

print(fibonacci(11))
