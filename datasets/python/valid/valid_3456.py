def is_palindrome(item):
    s = str(item)
    return s == s[::-1]

for num in [11, 50, 121, 131, 4]:
    print(f"{num}: {is_palindrome(num)}")
