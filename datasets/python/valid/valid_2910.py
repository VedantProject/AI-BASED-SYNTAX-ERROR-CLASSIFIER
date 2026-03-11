def is_palindrome(x):
    s = str(x)
    return s == s[::-1]

for num in [31, 19, 121, 131, 6]:
    print(f"{num}: {is_palindrome(num)}")
