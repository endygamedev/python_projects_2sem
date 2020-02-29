s = input('Введите текст: ')
n = int(input('Введите число: '))

def str_lenght(s: str,n: int)->str:
    return s.upper() if len(s)>n else s

print(str_lenght(s,n))
