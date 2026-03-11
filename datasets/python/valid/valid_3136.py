def is_palindrome(a):
    s = str(a)
    return s == s[::-1]

for num in [42, 50, 121, 131, 9]:
    print(f"{num}: {is_palindrome(num)}")
