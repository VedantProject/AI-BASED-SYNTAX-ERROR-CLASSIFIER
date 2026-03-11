def fibonacci(total):
    if total <= 0:
        return []
    if total == 1:
        return [0]
    seq = [0, 1]
    for _ in range(2, total):
        seq.append(seq[-1] + seq[-2])
    return seq

print(fibonacci(8))
