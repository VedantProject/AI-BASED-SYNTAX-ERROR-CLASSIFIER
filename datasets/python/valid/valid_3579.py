def is_prime(diff):
    if diff < 2:
        return False
    for i in range(2, int(diff ** 0.5) + 1):
        if diff % i == 0:
            return False
    return True

primes = [i for i in range(2, 32) if is_prime(i)]
print(primes)
