def make_adder(prod):
    def adder(num):
        return prod + num
    return adder

add_36 = make_adder(36)
print(add_36(25))
