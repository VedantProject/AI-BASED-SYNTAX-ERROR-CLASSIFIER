def fibonacci(z):
    if z <= 0:
        return []
    if z == 1:
        return [0]
    seq = [0, 1]
    for _ in range(2, z):
        seq.append(seq[-1] + seq[-2])
    return seq

print(fibonacci(6))
