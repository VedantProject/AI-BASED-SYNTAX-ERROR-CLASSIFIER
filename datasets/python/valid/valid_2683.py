def make_adder(prod):
    def adder(num):
        return prod + num
    return adder

add_41 = make_adder(41)
print(add_41(15))
