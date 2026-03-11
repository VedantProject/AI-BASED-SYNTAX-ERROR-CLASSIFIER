def is_prime(data):
    if data < 2:
        return False
    for i in range(2, int(data ** 0.5) + 1):
        if data % i == 0:
            return False
    return True

primes = [i for i in range(2, 17) if is_prime(i)]
print(primes)
