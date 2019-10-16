def infinite_num():
    num = 0
    while True:
        yield num
        num += 1

def is_palindrome(num):
    if num // 10 == 0:
        return False
    temp = num
    reversed_num = 0

    while temp != 0:
        reversed_num = (reversed_num * 10) + (temp % 10)
        temp = temp // 10

    if num == reversed_num:
        return True
    else:
        return False

def infinite_palindromes():
    num = 0
    while True:
        if is_palindrome(num):
            i = (yield  num)
            if i is not None:
                num = i
        num += 1


number = infinite_num()

print(next(number))
print(next(number))
print(next(number))

# for i in infinite_num():
#     if is_palindrome(i):
#         print(i)

print([i * 2 for i in range(10)])


pal_gen = infinite_palindromes()
for i in pal_gen:
    print(i)
    digits = len(str(i))
    pal_gen.send(10 ** (digits))

