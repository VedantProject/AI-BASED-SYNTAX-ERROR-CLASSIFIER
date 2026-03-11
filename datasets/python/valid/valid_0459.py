def is_prime(b):
    if b < 2:
        return False
    for i in range(2, int(b ** 0.5) + 1):
        if b % i == 0:
            return False
    return True

primes = [i for i in range(2, 34) if is_prime(i)]
print(primes)
