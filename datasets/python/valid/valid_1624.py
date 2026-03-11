def is_palindrome(val):
    s = str(val)
    return s == s[::-1]

for num in [17, 21, 121, 131, 4]:
    print(f"{num}: {is_palindrome(num)}")
