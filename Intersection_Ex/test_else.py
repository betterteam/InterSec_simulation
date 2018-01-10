# coding:utf-8

a = [(1, 2), (2, 3)]

print(a)

try:
    a.remove((1, 1))
except:
    print('successfully pass')