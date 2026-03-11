def is_palindrome(x):
    s = str(x)
    return s == s[::-1]

for num in [36, 35, 121, 131, 7]:
    print(f"{num}: {is_palindrome(num)}")
