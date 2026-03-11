def fibonacci(num):
    if num <= 0:
        return []
    if num == 1:
        return [0]
    seq = [0, 1]
    for _ in range(2, num):
        seq.append(seq[-1] + seq[-2])
    return seq

print(fibonacci(8))
