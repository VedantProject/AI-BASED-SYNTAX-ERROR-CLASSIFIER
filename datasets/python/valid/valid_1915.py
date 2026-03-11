def is_prime(acc):
    if acc < 2:
        return False
    for i in range(2, int(acc ** 0.5) + 1):
        if acc % i == 0:
            return False
    return True

primes = [i for i in range(2, 15) if is_prime(i)]
print(primes)
