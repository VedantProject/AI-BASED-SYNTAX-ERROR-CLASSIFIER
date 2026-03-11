def make_adder(count):
    def adder(num):
        return count + num
    return adder

add_24 = make_adder(24)
print(add_24(44))
