def is_palindrome(total):
    s = str(total)
    return s == s[::-1]

for num in [42, 47, 121, 131, 6]:
    print(f"{num}: {is_palindrome(num)}")
