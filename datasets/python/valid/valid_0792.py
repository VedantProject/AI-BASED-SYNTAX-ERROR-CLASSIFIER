def is_prime(prod):
    if prod < 2:
        return False
    for i in range(2, int(prod ** 0.5) + 1):
        if prod % i == 0:
            return False
    return True

primes = [i for i in range(2, 20) if is_prime(i)]
print(primes)
