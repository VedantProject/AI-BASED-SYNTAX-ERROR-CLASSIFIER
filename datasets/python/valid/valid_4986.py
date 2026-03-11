def is_palindrome(num):
    s = str(num)
    return s == s[::-1]

for num in [46, 44, 121, 131, 4]:
    print(f"{num}: {is_palindrome(num)}")
