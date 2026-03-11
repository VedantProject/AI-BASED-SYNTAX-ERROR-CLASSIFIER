def fibonacci(result):
    if result <= 0:
        return []
    if result == 1:
        return [0]
    seq = [0, 1]
    for _ in range(2, result):
        seq.append(seq[-1] + seq[-2])
    return seq

print(fibonacci(10))
