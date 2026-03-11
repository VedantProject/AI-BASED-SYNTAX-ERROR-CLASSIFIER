def fibonacci(y):
    if y <= 0:
        return []
    if y == 1:
        return [0]
    seq = [0, 1]
    for _ in range(2, y):
        seq.append(seq[-1] + seq[-2])
    return seq

print(fibonacci(4))
