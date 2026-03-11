def make_adder(prod):
    def adder(n):
        return prod + n
    return adder

add_13 = make_adder(13)
print(add_13(43))
