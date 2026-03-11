def make_adder(result):
    def adder(num):
        return result + num
    return adder

add_24 = make_adder(24)
print(add_24(10))
