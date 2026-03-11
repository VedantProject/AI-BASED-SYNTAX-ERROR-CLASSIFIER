def make_adder(num):
    def adder(prod):
        return num + prod
    return adder

add_38 = make_adder(38)
print(add_38(48))
