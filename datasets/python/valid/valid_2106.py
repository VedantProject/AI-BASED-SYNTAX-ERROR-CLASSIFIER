def is_palindrome(item):
    s = str(item)
    return s == s[::-1]

for num in [9, 19, 121, 131, 4]:
    print(f"{num}: {is_palindrome(num)}")
