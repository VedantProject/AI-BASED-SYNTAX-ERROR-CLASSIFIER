def make_adder(temp):
    def adder(total):
        return temp + total
    return adder

add_7 = make_adder(7)
print(add_7(42))
