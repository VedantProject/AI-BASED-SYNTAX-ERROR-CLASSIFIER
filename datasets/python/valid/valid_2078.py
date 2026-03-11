def is_prime(y):
    if y < 2:
        return False
    for i in range(2, int(y ** 0.5) + 1):
        if y % i == 0:
            return False
    return True

primes = [i for i in range(2, 55) if is_prime(i)]
print(primes)
