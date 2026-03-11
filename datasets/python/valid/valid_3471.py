def is_palindrome(result):
    s = str(result)
    return s == s[::-1]

for num in [33, 40, 121, 131, 4]:
    print(f"{num}: {is_palindrome(num)}")
