def make_adder(count):
    def adder(data):
        return count + data
    return adder

add_29 = make_adder(29)
print(add_29(9))
