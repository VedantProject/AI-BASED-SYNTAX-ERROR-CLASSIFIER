def make_adder(z):
    def adder(res):
        return z + res
    return adder

add_50 = make_adder(50)
print(add_50(42))
