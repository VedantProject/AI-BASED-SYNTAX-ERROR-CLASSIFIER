def make_adder(n):
    def adder(total):
        return n + total
    return adder

add_9 = make_adder(9)
print(add_9(49))
