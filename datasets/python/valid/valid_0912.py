def make_adder(acc):
    def adder(total):
        return acc + total
    return adder

add_42 = make_adder(42)
print(add_42(13))
