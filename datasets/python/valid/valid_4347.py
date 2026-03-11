def make_adder(diff):
    def adder(total):
        return diff + total
    return adder

add_9 = make_adder(9)
print(add_9(10))
