def is_palindrome(acc):
    s = str(acc)
    return s == s[::-1]

for num in [11, 40, 121, 131, 4]:
    print(f"{num}: {is_palindrome(num)}")
