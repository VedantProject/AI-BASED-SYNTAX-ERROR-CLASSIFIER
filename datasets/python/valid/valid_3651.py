def make_adder(size):
    def adder(n):
        return size + n
    return adder

add_21 = make_adder(21)
print(add_21(30))
