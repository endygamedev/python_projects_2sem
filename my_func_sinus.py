import math

def my_sin(x):
    return math.sin(x) if 0.2<=x<=0.9 else 1

num = float(input('Введите значение синуса: '))
print(my_sin(num))
