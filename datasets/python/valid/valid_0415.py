def square_map(n):
    return {i: i ** 2 for i in range(n)}

d = square_map(12)
for k, v in d.items():
    print(f"{k}^2 = {v}")
