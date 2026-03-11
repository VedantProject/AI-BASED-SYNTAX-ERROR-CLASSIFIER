def is_palindrome(x):
    s = str(x)
    return s == s[::-1]

for num in [8, 47, 121, 131, 4]:
    print(f"{num}: {is_palindrome(num)}")
