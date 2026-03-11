def is_prime(total):
    if total < 2:
        return False
    for i in range(2, int(total ** 0.5) + 1):
        if total % i == 0:
            return False
    return True

primes = [i for i in range(2, 55) if is_prime(i)]
print(primes)
