def make_adder(prod):
    def adder(result):
        return prod + result
    return adder

add_2 = make_adder(2)
print(add_2(7))
