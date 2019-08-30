# # import pandas as pd
# #
# # dict = {"country": ["Brazil", "Russia", "India", "China", "South Africa"],
# #        "capital": ["Brasilia", "Moscow", "New Dehli", "Beijing", "Pretoria"],
# #        "area": [8.516, 17.10, 3.286, 9.597, 1.221],
# #        "population": [200.4, 143.5, 1252, 1357, 52.98]
# #         }
# #
# # brics = pd.DataFrame(dict)
# # brics.index = ["BR", "RU", "IN", "CH", "SA"]
# # print(brics)
# # print()
# # print(brics.loc['IN'])
# # print()
# # print(brics.iloc[2])
#
# height = [1.87,  1.87, 1.82, 1.91, 1.90, 1.85]
# weight = [81.65, 97.52, 95.25, 92.98, 86.18, 88.45]
#
# import numpy as np
#
# np_height = np.array(height)
# np_weight = np.array(weight)
#
# bmi = np_weight / np_height ** 2
#
# print(height)
# print(np_height)
# print(np_weight)
# print(bmi)
#
# print(bmi[bmi > 25])
#
# weight_kg = [81.65, 97.52, 95.25, 92.98, 86.18, 88.45]
#
# np_weight_kg = np.array(weight_kg)
#
# np_weight_pd = np_weight_kg * 2.2
#
# print(np_weight_pd)
#
#
# print('-----------------------')

import random


def lottery():
    for i in range(6):
        yield random.randint(1, 40)

    yield random.randint(55, 80)


for random_number in lottery():
    print('And the nexe number is... %d!' %(random_number))


def fibonacci(length):
    a = 1
    b = 1
    yield a
    yield b
    for i in range(length-2):
        b, a = a, b
        b = a + b
        yield b


for i in fibonacci(10):
    print(i)

numbers = [34.6, -203.4, 44.9, 68.3, -12.2, 44.6, 12.7]
newlist = [num for num in numbers if num > 0]
print(newlist)

# def foo(first, second, third, *therest):
#     print("First: %s" %(first))
#     print("Second: %s" %(second))
#     print("Third: %s" %(third))
#     print("And all the rest... %s" %(list(therest)))
#
#
# foo(1,2,3,4,5)

# edit the functions prototype and implementation
def foo(a, b, c, *therest):
    if len(list(therest)) != 0:
        return len(list(therest))
    else:
        return 0
    pass

def bar(a, b, c, **options):
    if options.get('magicnumber') == 7:
        return True
    return False
    pass


# test code
if foo(1,2,3,4) == 1:
    print("Good.")
if foo(1,2,3,4,5) == 2:
    print("Better.")
if bar(1,2,3,magicnumber = 6) == False:
    print("Great.")
if bar(1,2,3,magicnumber = 7) == True:
    print("Awesome!")

a = ["Jake", "John", "Eric"]
b = ["John", "Jill"]

a = set(a)
b = set(b)

print(a.difference(b))

#Following is the exercise, function provided:
from functools import partial
def func(u,v,w,x):
    return u*4 + v*3 + w*2 + x

exe = partial(func, 10, 3, 5)
print(exe(1))
#Enter your code here to create and print with your partial function