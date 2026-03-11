def make_adder(acc):
    def adder(diff):
        return acc + diff
    return adder

add_41 = make_adder(41)
print(add_41(9))
