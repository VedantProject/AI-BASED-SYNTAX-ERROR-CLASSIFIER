def is_palindrome(count):
    s = str(count)
    return s == s[::-1]

for num in [41, 17, 121, 131, 4]:
    print(f"{num}: {is_palindrome(num)}")
