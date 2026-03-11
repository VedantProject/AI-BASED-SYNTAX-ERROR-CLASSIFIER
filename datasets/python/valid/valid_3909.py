def is_palindrome(x):
    s = str(x)
    return s == s[::-1]

for num in [35, 32, 121, 131, 2]:
    print(f"{num}: {is_palindrome(num)}")
