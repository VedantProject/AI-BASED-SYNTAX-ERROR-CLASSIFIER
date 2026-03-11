def fibonacci(b):
    if b <= 0:
        return []
    if b == 1:
        return [0]
    seq = [0, 1]
    for _ in range(2, b):
        seq.append(seq[-1] + seq[-2])
    return seq

print(fibonacci(11))
