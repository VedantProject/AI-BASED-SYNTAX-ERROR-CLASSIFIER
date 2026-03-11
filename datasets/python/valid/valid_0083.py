def is_prime(res):
    if res < 2:
        return False
    for i in range(2, int(res ** 0.5) + 1):
        if res % i == 0:
            return False
    return True

primes = [i for i in range(2, 23) if is_prime(i)]
print(primes)
