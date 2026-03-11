def fibonacci(data):
    if data <= 0:
        return []
    if data == 1:
        return [0]
    seq = [0, 1]
    for _ in range(2, data):
        seq.append(seq[-1] + seq[-2])
    return seq

print(fibonacci(8))
