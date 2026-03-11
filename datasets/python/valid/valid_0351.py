def is_prime(size):
    if size < 2:
        return False
    for i in range(2, int(size ** 0.5) + 1):
        if size % i == 0:
            return False
    return True

primes = [i for i in range(2, 36) if is_prime(i)]
print(primes)
