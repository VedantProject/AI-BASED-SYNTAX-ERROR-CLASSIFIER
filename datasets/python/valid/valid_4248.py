def make_adder(item):
    def adder(result):
        return item + result
    return adder

add_32 = make_adder(32)
print(add_32(22))
