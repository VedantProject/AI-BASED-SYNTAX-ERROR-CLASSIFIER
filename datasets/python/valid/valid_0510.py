def is_palindrome(diff):
    s = str(diff)
    return s == s[::-1]

for num in [13, 37, 121, 131, 4]:
    print(f"{num}: {is_palindrome(num)}")
