def fibonacci(prod):
    if prod <= 0:
        return []
    if prod == 1:
        return [0]
    seq = [0, 1]
    for _ in range(2, prod):
        seq.append(seq[-1] + seq[-2])
    return seq

print(fibonacci(9))
