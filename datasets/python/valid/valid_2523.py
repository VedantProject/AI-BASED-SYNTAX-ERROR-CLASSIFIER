def is_palindrome(a):
    s = str(a)
    return s == s[::-1]

for num in [50, 9, 121, 131, 2]:
    print(f"{num}: {is_palindrome(num)}")
