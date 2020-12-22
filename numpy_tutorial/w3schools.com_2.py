x = [1, 2, 3, 4]
y = [4, 5, 6, 7]
z = []

for i, j in zip(x, y):
  z.append(i + j)
print(z)

import numpy as np

print(np.add(x, y))
print(type(np.concatenate))
if type(np.add) == np.ufunc:
  print('add is ufunc')
else:
  print('add is not ufunc')


arr1 = np.array([10, 11, 12, 13, 14, 15])
arr2 = np.array([20, 21, 22, 23, 24, 25])
newarr = np.add(arr1, arr2)
print(newarr)

arr1 = np.array([10, 20, 30, 40, 50, 60])
arr2 = np.array([3, 7, 9, 8, 2, 33])
newarr = np.remainder(arr1, arr2)
newarr1 = np.mod(arr1, arr2)
print(newarr)
print(newarr1)
print(np.divmod(arr1, arr2))

arr = np.trunc([-3.1666, 3.6667])
print(arr)
arr = np.fix([-3.1666, 3.6667])
print(arr)

arr1 = np.array([1, 2, 3])
arr2 = np.array([1, 2, 3])
newarr = np.sum([arr1, arr2], axis=1)
print(newarr)

arr = np.array([1, 2, 3])
newarr = np.cumsum(arr)
print(newarr)

arr = np.array([1, 2, 3, 4])
x = np.prod(arr)
print(x)

arr1 = np.array([1, 2, 3, 4])
arr2 = np.array([5, 6, 7, 8])
x = np.prod([arr1, arr2])
print(x)

arr1 = np.array([1, 2, 3, 4])
arr2 = np.array([5, 6, 7, 8])
newarr = np.prod([arr1, arr2], axis=1)
print(newarr)

arr = np.array([5, 6, 7, 8])
newarr = np.cumprod(arr)
print(newarr)

arr = np.array([10, 15, 25, 5])
newarr = np.diff(arr)
print(newarr)

arr = np.array([10, 15, 25, 5])
newarr = np.diff(arr, n=2)
print(newarr)

num1 = 4
num2 = 6
x = np.lcm(num1, num2)
print(x)

arr = np.arange(1, 11)
x = np.lcm.reduce(arr)
print(x)

num1 = 6
num2 = 9
x = np.gcd(num1, num2)

print(x)
arr = np.array([90, 180, 270, 360])
x = np.deg2rad(arr)
print(x)

base = 3
perp = 4
x = np.hypot(base, perp)
print(x)

arr1 = np.array([1, 2, 3, 4])
arr2 = np.array([3, 4, 5, 6])
newarr = np.union1d(arr1, arr2)
print(newarr)


newarr = np.intersect1d(arr1, arr2, assume_unique=True)
print(newarr)

newarr = np.setdiff1d(arr1, arr2, assume_unique=True)
print(newarr)

set1 = np.array([1, 2, 3, 4])
set2 = np.array([3, 4, 5, 6])
newarr = np.setxor1d(set1, set2, assume_unique=True)
print(newarr)