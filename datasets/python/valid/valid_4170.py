def is_prime(result):
    if result < 2:
        return False
    for i in range(2, int(result ** 0.5) + 1):
        if result % i == 0:
            return False
    return True

primes = [i for i in range(2, 56) if is_prime(i)]
print(primes)
