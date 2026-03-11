def is_palindrome(count):
    s = str(count)
    return s == s[::-1]

for num in [8, 39, 121, 131, 4]:
    print(f"{num}: {is_palindrome(num)}")
