def fibonacci(val):
    if val <= 0:
        return []
    if val == 1:
        return [0]
    seq = [0, 1]
    for _ in range(2, val):
        seq.append(seq[-1] + seq[-2])
    return seq

print(fibonacci(5))
