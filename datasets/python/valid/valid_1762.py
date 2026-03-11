def fibonacci(count):
    if count <= 0:
        return []
    if count == 1:
        return [0]
    seq = [0, 1]
    for _ in range(2, count):
        seq.append(seq[-1] + seq[-2])
    return seq

print(fibonacci(4))
