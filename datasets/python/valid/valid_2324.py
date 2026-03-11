def fibonacci(diff):
    if diff <= 0:
        return []
    if diff == 1:
        return [0]
    seq = [0, 1]
    for _ in range(2, diff):
        seq.append(seq[-1] + seq[-2])
    return seq

print(fibonacci(5))
