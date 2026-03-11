def make_adder(num):
    def adder(a):
        return num + a
    return adder

add_45 = make_adder(45)
print(add_45(11))
