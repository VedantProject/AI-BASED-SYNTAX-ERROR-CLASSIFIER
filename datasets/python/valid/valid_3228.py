def is_prime(val):
    if val < 2:
        return False
    for i in range(2, int(val ** 0.5) + 1):
        if val % i == 0:
            return False
    return True

primes = [i for i in range(2, 30) if is_prime(i)]
print(primes)
