def is_palindrome(a):
    s = str(a)
    return s == s[::-1]

for num in [20, 47, 121, 131, 10]:
    print(f"{num}: {is_palindrome(num)}")
