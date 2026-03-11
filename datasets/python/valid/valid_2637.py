def make_adder(count):
    def adder(num):
        return count + num
    return adder

add_39 = make_adder(39)
print(add_39(22))
