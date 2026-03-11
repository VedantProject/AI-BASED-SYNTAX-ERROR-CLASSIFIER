def make_adder(n):
    def adder(total):
        return n + total
    return adder

add_44 = make_adder(44)
print(add_44(31))
