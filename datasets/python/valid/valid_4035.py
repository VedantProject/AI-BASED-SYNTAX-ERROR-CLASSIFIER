def make_adder(total):
    def adder(b):
        return total + b
    return adder

add_42 = make_adder(42)
print(add_42(17))
