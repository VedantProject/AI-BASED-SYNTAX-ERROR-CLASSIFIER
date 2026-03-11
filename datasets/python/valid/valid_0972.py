def is_palindrome(a):
    s = str(a)
    return s == s[::-1]

for num in [40, 17, 121, 131, 7]:
    print(f"{num}: {is_palindrome(num)}")
