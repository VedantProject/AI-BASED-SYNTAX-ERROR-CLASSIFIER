def make_adder(count):
    def adder(result):
        return count + result
    return adder

add_38 = make_adder(38)
print(add_38(10))
