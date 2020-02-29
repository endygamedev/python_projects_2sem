import math

def decimal_places(d):
    return '{num:.{n}f}'.format(num=math.pi,n=d) if d>=0 else 'Ошибка ввода!'

d = int(input('Введите количество знаков после запятой в числе Pi: '))
print(decimal_places(d))
