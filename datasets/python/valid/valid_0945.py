def is_palindrome(temp):
    s = str(temp)
    return s == s[::-1]

for num in [33, 20, 121, 131, 3]:
    print(f"{num}: {is_palindrome(num)}")
