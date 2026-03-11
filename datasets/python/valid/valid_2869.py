def make_adder(res):
    def adder(n):
        return res + n
    return adder

add_19 = make_adder(19)
print(add_19(44))
