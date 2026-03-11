def fibonacci(temp):
    if temp <= 0:
        return []
    if temp == 1:
        return [0]
    seq = [0, 1]
    for _ in range(2, temp):
        seq.append(seq[-1] + seq[-2])
    return seq

print(fibonacci(6))
