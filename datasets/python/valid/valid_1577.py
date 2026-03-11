def is_palindrome(total):
    s = str(total)
    return s == s[::-1]

for num in [36, 42, 121, 131, 10]:
    print(f"{num}: {is_palindrome(num)}")
