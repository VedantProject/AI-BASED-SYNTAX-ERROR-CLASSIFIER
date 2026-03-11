def is_prime(count):
    if count < 2:
        return False
    for i in range(2, int(count ** 0.5) + 1):
        if count % i == 0:
            return False
    return True

primes = [i for i in range(2, 19) if is_prime(i)]
print(primes)
