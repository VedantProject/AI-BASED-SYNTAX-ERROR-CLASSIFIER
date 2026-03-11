def fibonacci(acc):
    if acc <= 0:
        return []
    if acc == 1:
        return [0]
    seq = [0, 1]
    for _ in range(2, acc):
        seq.append(seq[-1] + seq[-2])
    return seq

print(fibonacci(9))
