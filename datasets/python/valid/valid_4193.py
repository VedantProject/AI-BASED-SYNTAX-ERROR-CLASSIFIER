def is_prime(m):
    if m < 2:
        return False
    for i in range(2, int(m ** 0.5) + 1):
        if m % i == 0:
            return False
    return True

primes = [i for i in range(2, 30) if is_prime(i)]
print(primes)
