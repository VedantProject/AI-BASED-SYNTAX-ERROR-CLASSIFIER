def make_adder(size):
    def adder(num):
        return size + num
    return adder

add_48 = make_adder(48)
print(add_48(13))
