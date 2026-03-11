def is_prime(item):
    if item < 2:
        return False
    for i in range(2, int(item ** 0.5) + 1):
        if item % i == 0:
            return False
    return True

primes = [i for i in range(2, 29) if is_prime(i)]
print(primes)
