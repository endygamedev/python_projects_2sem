# https://drakonhub.com/ide/doc/endy/2 - ссылка на ДРАКОН-схему

import random
rnd = random.randint(1,4)
num = int(input('Введите число: '))

while rnd != num:
    if rnd>num:
        num = int(input('Попробуйте ещё раз!\nВведите большее число:'))
    else:
        num = int(input('Попробуйте ещё раз!\nВведите меньшее число:'))
print('Победа!')
