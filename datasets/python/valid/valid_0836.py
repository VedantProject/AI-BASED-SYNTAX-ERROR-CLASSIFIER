def is_prime(temp):
    if temp < 2:
        return False
    for i in range(2, int(temp ** 0.5) + 1):
        if temp % i == 0:
            return False
    return True

primes = [i for i in range(2, 34) if is_prime(i)]
print(primes)
