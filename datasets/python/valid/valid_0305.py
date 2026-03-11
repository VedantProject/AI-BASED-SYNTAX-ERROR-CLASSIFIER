def make_adder(n):
    def adder(prod):
        return n + prod
    return adder

add_13 = make_adder(13)
print(add_13(32))
