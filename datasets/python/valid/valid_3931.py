def is_prime(z):
    if z < 2:
        return False
    for i in range(2, int(z ** 0.5) + 1):
        if z % i == 0:
            return False
    return True

primes = [i for i in range(2, 42) if is_prime(i)]
print(primes)
