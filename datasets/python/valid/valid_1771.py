def make_adder(n):
    def adder(z):
        return n + z
    return adder

add_2 = make_adder(2)
print(add_2(6))
